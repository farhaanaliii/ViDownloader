import time

from PyQt5.QtCore import (
    QMetaObject,
    QObject,
    QThread,
    QTimer,
    Qt,
    pyqtSignal,
    pyqtSlot,
)

from vidownloader.core.Constants import EventType, Status, WorkerType
from vidownloader.core.Logger import get_logger
from vidownloader.core.Models import DownloaderEvent, Link, ScraperEvent
from vidownloader.core.VSettings import get_download_threads
from vidownloader.core.Worker import Downloader, Scraper

logger = get_logger("Worker")


class Worker(QThread):
    error_message = pyqtSignal(str)
    on_finish = pyqtSignal(str, int)

    def __init__(self):
        super().__init__()
        self._stop_requested = False

    def run(self):
        raise NotImplementedError("Subclasses must implement this method")

    def stop(self):
        self._stop_requested = True
        self.requestInterruption()


class ScraperWorker(Worker):
    _event = pyqtSignal(ScraperEvent)
    update_progress = pyqtSignal(int)

    def __init__(self, links: list[Link]):
        super().__init__()
        self.links = links
        self.scraper = None

    def run(self):
        try:
            for i, link in enumerate(self.links):
                if self.isInterruptionRequested() or self._stop_requested:
                    self.on_finish.emit("Scraping stopped by user.", WorkerType.SCRAPER)
                    return

                self.scraper = Scraper.Scraper(link)
                self.scraper._event.connect(self._event)
                self.scraper.start()

                self.update_progress.emit(i + 1)

            if not (self.isInterruptionRequested() or self._stop_requested):
                self.on_finish.emit("Scraping completed.", WorkerType.SCRAPER)
        except Exception as e:
            self.error_message.emit(f"Scraping error: {str(e)}")

    def stop(self):
        if self.scraper:
            self.scraper.set_stop()
        super().stop()


class DownloaderWorker(Worker):
    _event = pyqtSignal(DownloaderEvent)
    update_progress = pyqtSignal(int)

    def __init__(self, links: list[Link]):
        super().__init__()
        self.links = links
        self.current_index = 0
        self.active_threads = 0
        self.finished_threads = 0
        self.threads: list[Downloader.Downloader] = []
        self.is_paused = False

    def run(self):
        logger.info("DownloadProcess started.")
        self._start_next_batch()
        self.exec_()

    def _start_next_batch(self):
        if self.is_paused or self._stop_requested:
            return

        max_threads = get_download_threads()
        while self.active_threads < max_threads and self.current_index < len(
            self.links
        ):
            if self._stop_requested:
                return

            link = self.links[self.current_index]
            self.current_index += 1

            thread = Downloader.Downloader(link)
            thread._event.connect(self.event_handler)
            logger.debug("Starting the downloader thread for : %s", link.url)
            thread.start()
            logger.info(f"Download thread for {link} started")
            self.threads.append(thread)
            self.active_threads += 1

    def stop(self):
        super().stop()
        for thread in self.threads:
            if thread.isRunning():
                thread.requestInterruption()
        self.quit()

    def pause(self):
        logger.info("Pausing all downloader threads.")
        self.is_paused = True

    def resume(self):
        logger.info("Resuming downloader threads.")
        self.is_paused = False
        self._start_next_batch()

    @pyqtSlot(DownloaderEvent)
    def event_handler(self, event: DownloaderEvent):
        if event.event == EventType.STATUS and event.status in (
            Status.COMPLETED,
            Status.FAILED,
        ):
            self.finished_threads += 1
            self.active_threads -= 1
            self.update_progress.emit(self.finished_threads)

            self.threads = [t for t in self.threads if t.isRunning()]

            if not self._stop_requested and self.current_index < len(self.links):
                QTimer.singleShot(0, self._start_next_batch)

        self._event.emit(event)

        if self.finished_threads >= len(self.links) and not self._stop_requested:
            logger.info("DownloadProcess completed.")
            self.on_finish.emit("Download completed.", WorkerType.DOWNLOADER)
            self.quit()

