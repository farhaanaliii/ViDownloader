from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QMessageBox

from vidownloader.core import Constants, Logger, Utils, VSettings
from vidownloader.core.Models import *
from vidownloader.core.VIIO import VIIO, InvalidFileError, VIIOError
from vidownloader.ui import home_ui
from vidownloader.window.MainWindow import MainWindow

logger = Logger.get_logger("HomeWindow")


class HomeWindow(home_ui.HOME_UI):
    def __init__(self):
        super().__init__()
        logger.info("initialized")
        self.main = None
        self.init_handlers()

    def init_handlers(self):
        self.start_button.clicked.connect(self.action_start)
        self.import_button.clicked.connect(self.action_import)

    def action_start(self):
        links = self.text_area.toPlainText().strip()
        if not links:
            QMessageBox.warning(
                self, "Warning", "Please enter at least one link to download."
            )
            return

        filtered_links = Utils.parse_links(links)
        if not filtered_links:
            QMessageBox.warning(self, "Warning", "No valid links found.")
            return

        self.main = MainWindow(
            Bridge(bridge_type=BridgeType.LINKS, links=filtered_links)
        )
        self.main.setAttribute(Qt.WA_DeleteOnClose)
        self.main.show()
        self.close()

    def action_import(self):
        default_dir = Path(VSettings.get_export_location())
        default_dir.mkdir(parents=True, exist_ok=True)

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Videos",
            str(default_dir),
            f"{Constants.App.NAME} Files (*{VIIO.EXTENSION});;All Files (*)",
        )

        if not file_path:
            return

        try:
            videos = VIIO.quick_load(file_path)

            if not videos:
                QMessageBox.warning(
                    self, "Warning", "The selected file contains no videos."
                )
                return

            logger.info(f"Imported {len(videos)} videos from: {file_path}")

            self.main = MainWindow(
                Bridge(bridge_type=BridgeType.IMPORTED, videos=videos)
            )
            self.main.show()
            self.main.setAttribute(Qt.WA_DeleteOnClose)
            self.close()

        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"File not found: {file_path}")
            logger.error(f"Import failed - file not found: {file_path}")

        except InvalidFileError as e:
            QMessageBox.critical(
                self,
                "Invalid File",
                f"The selected file is not a valid ViDownloader export file.\n\n{str(e)}",
            )
            logger.error(f"Import failed - invalid file: {e}")

        except VIIOError as e:
            QMessageBox.critical(
                self, "Import Error", f"Failed to import file:\n\n{str(e)}"
            )
            logger.error(f"Import failed: {e}")

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"An unexpected error occurred:\n\n{str(e)}"
            )
            logger.error(f"Import failed with unexpected error: {e}")
