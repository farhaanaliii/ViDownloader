from pathlib import Path

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QTreeWidgetItem

from vidownloader.core import Constants, Logger, Utils, VSettings, Worker
from vidownloader.core.Models import *
from vidownloader.core.VIIO import VIIO, VIIOError
from vidownloader.ui import main_ui

logger = Logger.get_logger("MainWindow")


class MainWindow(main_ui.MAIN_UI):
    def __init__(self, bridge: Bridge):
        super().__init__()

        self.installEventFilter(self)

        self.scraper_t = None
        self.downloader_t = None
        self.is_paused = False
        self.selected_links: list[Link] = []

        if bridge.bridge_type == BridgeType.LINKS:
            self.links = bridge.links
            self.action_start_scraping()
        elif bridge.bridge_type == BridgeType.IMPORTED:
            self.import_videos(bridge.videos)

        self.init_click_handlers()
        logger.info("initialized")

    def init_click_handlers(self):
        self.stop_button.clicked.connect(self.action_stop)
        self.tree_widget.itemSelectionChanged.connect(
            lambda: setattr(
                self,
                "selected_links",
                [
                    Utils.treeitem_to_link(item)
                    for item in self.tree_widget.selectedItems()
                ],
            )
        )
        self.select_all_button.clicked.connect(self.tree_widget.selectAll)
        self.deselect_button.clicked.connect(self.tree_widget.clearSelection)
        self.download_button.clicked.connect(self.action_start_downloading)
        self.export_button.clicked.connect(self.action_export)
        self.stop_button.clicked.connect(self.action_stop)
        self.pause_button.clicked.connect(self.action_pause)
        self.resume_button.clicked.connect(self.action_resume)

    def go_back(self):
        scraper_running = (
            hasattr(self, "scraper_t")
            and self.scraper_t is not None
            and self.scraper_t.isRunning()
        )
        downloader_running = (
            hasattr(self, "downloader_t")
            and self.downloader_t is not None
            and self.downloader_t.isRunning()
        )

        if scraper_running or downloader_running:
            QMessageBox.warning(
                self,
                "Process Running",
                "Please stop the running process before going back.\n\nClick the 'Stop' button to stop the current operation.",
            )
            return

        reply = QMessageBox.question(
            self,
            "Confirm Go Back",
            "Are you sure you want to go back to the home screen?\n\nAny unsaved progress will be lost.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            self.cleanup_threads()

            app = QApplication.instance()

            if hasattr(app, "home_window"):
                app.home_window.show()

            self.close()

    def import_videos(self, videos: list[Video]):
        if not videos:
            QMessageBox.warning(self, "Warning", "No videos in the imported file!")
            return

        self.set_status(
            f"Imported {len(videos)} videos!", Constants.StatusColors.SUCCESS
        )
        self.signal_append_videos(videos)

        logger.info(f"Imported {len(videos)} videos from VIIO file")

    def action_export(self):
        video_count = self.tree_widget.topLevelItemCount()

        if video_count == 0:
            QMessageBox.warning(self, "Warning", "No videos to export!")
            return

        default_dir = Path(VSettings.get_export_location())
        default_dir.mkdir(parents=True, exist_ok=True)
        export_location = default_dir / Utils.generate_export_filename()

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Videos",
            str(export_location),
            f"{Constants.App.NAME} Files (*{VIIO.EXTENSION});;All Files (*)",
        )

        if not file_path:
            return

        try:
            videos = []
            for i in range(video_count):
                item = self.tree_widget.topLevelItem(i)
                video = Utils.treeitem_to_video(item)
                videos.append(video)

            saved_path = VIIO.quick_save(videos, file_path)

            QMessageBox.information(
                self,
                "Export Successful",
                f"Successfully exported {len(videos)} videos to:\n{saved_path}",
            )
            logger.info(f"Exported {len(videos)} videos to: {saved_path}")

        except VIIOError as e:
            QMessageBox.critical(
                self, "Export Error", f"Failed to export videos:\n\n{str(e)}"
            )
            logger.error(f"Export failed: {e}")

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"An unexpected error occurred:\n\n{str(e)}"
            )
            logger.error(f"Export failed with unexpected error: {e}")

    def action_start_scraping(self):
        if not self.links:
            QMessageBox.warning(self, "Warning", "No links to process!")
            return

        self.set_status("Scraping...", Constants.StatusColors.INFO)
        self.progress_bar.setMaximum(len(self.links))
        self.progress_bar.setValue(0)
        self.scraper_t = Worker.ScraperWorker(self.links)
        self.scraper_t._event.connect(self.signal_event)
        self.scraper_t.error_message.connect(self.signal_on_error)
        self.scraper_t.update_progress.connect(self.update_progress)
        self.scraper_t.on_finish.connect(self.signal_on_finish)
        self.scraper_t.start()

        self.stop_button.setEnabled(True)

    def action_start_downloading(self):
        if not self.selected_links:
            QMessageBox.warning(self, "Warning", "Please select Videos to download.")
            return

        self.set_status("Downloading...", Constants.StatusColors.INFO)
        self.progress_bar.setMaximum(len(self.selected_links))
        self.progress_bar.setValue(0)
        self.downloader_t = Worker.DownloaderWorker(self.selected_links)
        self.downloader_t._event.connect(self.signal_event)
        self.downloader_t.on_finish.connect(self.signal_on_finish)
        self.downloader_t.error_message.connect(self.signal_on_error)
        self.downloader_t.update_progress.connect(self.update_progress)
        self.downloader_t.start()

        self.stop_button.setEnabled(True)
        self.pause_button.setEnabled(True)
        self.download_button.setEnabled(False)
        self.mark_pending_items()
        self.tree_widget.clearSelection()

    def signal_event(self, event: DownloaderEvent | ScraperEvent):
        # downloader events
        if isinstance(event, DownloaderEvent):
            item = self.find_item_by_id(event.video_id)
            if not item:
                logger.warning(f"Could not find ({event.video_id}) item to update")
                return

            if (
                event.event == Constants.EventType.PROGRESS
                and event.progress is not None
            ):
                self.set_video_progress(item, event.progress)
            elif event.event == Constants.EventType.STATUS and event.status is not None:
                self.set_video_status(item, event.status)
                if event.video_path is not None:
                    self.set_video_size(item, event.video_path)

        # scraper events
        elif event.event == Constants.EventType.VIDEOS:
            self.signal_append_videos(event.videos)
        elif event.event == Constants.EventType.MESSAGE:
            self.signal_on_error(event.message)

    def set_video_progress(self, item: QTreeWidgetItem, progress: str):
        item.setText(Constants.TreeViewColumns.PROGRESS, progress)

    def set_video_status(self, item: QTreeWidgetItem, status: Constants.Status):
        if status == Constants.Status.COMPLETED:
            self.change_item_color(item, Constants.StatusColors.SUCCESS)
        elif status == Constants.Status.FAILED:
            self.change_item_color(item, Constants.StatusColors.ERROR)
        elif status == Constants.Status.DOWNLOADING:
            self.change_item_color(item, Constants.StatusColors.WARNING)
        elif status == Constants.Status.STARTING:
            self.change_item_color(item, Constants.StatusColors.INFO)

        item.setText(Constants.TreeViewColumns.STATUS, status.value)

    def mark_pending_items(self):
        for link in self.selected_links:
            item = self.find_item_by_id(link.video_id)
            if item:
                self.change_item_color(item, Constants.StatusColors.PENDING)

    def find_item_by_id(self, video_id: str) -> QTreeWidgetItem | None:
        for i in range(self.tree_widget.topLevelItemCount()):
            item = self.tree_widget.topLevelItem(i)
            _id = item.text(Constants.TreeViewColumns.ID)
            if _id == video_id:
                return item

        return None

    def change_item_color(self, item: QTreeWidgetItem, color: QColor):
        for col in range(self.tree_widget.columnCount()):
            item.setData(col, Qt.BackgroundRole, color)

    @pyqtSlot(Video)
    def signal_append_videos(self, videos: list[Video]):
        start_index = self.tree_widget.topLevelItemCount()

        for i, video in enumerate(videos):
            video.no = start_index + i + 1
            item = Utils.video_to_treeitem(video)
            self.tree_widget.addTopLevelItem(item)

            if start_index == 0:
                self.download_button.setEnabled(True)

    @pyqtSlot(str)
    def signal_on_error(self, msg: str):
        self.stop_button.setEnabled(False)
        QMessageBox.critical(self, "Error", msg)

    def set_status(self, message: str, color: QColor):
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color.name()}; font-weight: bold;")

    @pyqtSlot(str, int)
    def signal_on_finish(self, msg: str, worker_type: int):
        self.set_status(msg, Constants.StatusColors.SUCCESS)
        self.stop_button.setEnabled(False)

        if worker_type == Constants.WorkerType.SCRAPER:
            if hasattr(self, "scraper_t") and self.scraper_t is not None:
                self.scraper_t.quit()
                self.scraper_t.wait()
                self.scraper_t = None
        elif worker_type == Constants.WorkerType.DOWNLOADER:
            if hasattr(self, "downloader_t") and self.downloader_t is not None:
                self.downloader_t.quit()
                self.downloader_t.wait()
                self.downloader_t = None

        self.download_button.setEnabled(True)

    def update_progress(self, value: int):
        self.progress_bar.setValue(value)

    def action_stop(self):
        self.set_status("Stopping...", Constants.StatusColors.WARNING)
        logger.info("Stop action initiated")

        if hasattr(self, "scraper_t") and self.scraper_t is not None:
            self.scraper_t.stop()
            if self.scraper_t.isRunning():
                self.scraper_t.wait(3000)  # Wait up to 3 seconds
            self.scraper_t = None

        if hasattr(self, "downloader_t") and self.downloader_t is not None:
            self.downloader_t.stop()
            if self.downloader_t.isRunning():
                self.downloader_t.wait(3000)  # Wait up to 3 seconds
            self.downloader_t = None

        self.stop_button.setEnabled(False)
        self.download_button.setEnabled(True)
        self.set_status("Stopped", Constants.StatusColors.ERROR)

    def action_pause(self):
        if self.downloader_t is not None and not self.is_paused:
            self.downloader_t.pause()
            self.is_paused = True
            self.set_status("Paused", Constants.StatusColors.WARNING)
            self.pause_button.setEnabled(False)
            self.resume_button.setEnabled(True)
            logger.info("Download paused")

    def action_resume(self):
        if self.downloader_t is not None and self.is_paused:
            self.downloader_t.resume()
            self.is_paused = False
            self.set_status("Downloading...", Constants.StatusColors.INFO)
            self.pause_button.setEnabled(True)
            self.resume_button.setEnabled(False)
            logger.info("Download resumed")

    def cleanup_threads(self):
        if hasattr(self, "scraper_t") and self.scraper_t is not None:
            self.scraper_t.stop()
            if self.scraper_t.isRunning():
                self.scraper_t.wait(5000)  # Wait up to 5 seconds
            self.scraper_t = None

        if hasattr(self, "downloader_t") and self.downloader_t is not None:
            self.downloader_t.stop()
            if self.downloader_t.isRunning():
                self.downloader_t.wait(5000)  # Wait up to 5 seconds
            self.downloader_t = None

    def closeEvent(self, event):
        self.cleanup_threads()
        super().closeEvent(event)

    def set_video_size(self, item: QTreeWidgetItem, video_path: Path):
        if video_path.exists():
            size_str = Utils.format_size(video_path.stat().st_size)
            item.setText(Constants.TreeViewColumns.SIZE, size_str)
        else:
            video_id = item.text(Constants.TreeViewColumns.ID)
            logger.warning(f"Video file for {video_id} does not exist: {video_path}")
