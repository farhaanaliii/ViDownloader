import time
from threading import Lock

from vidownloader.core.Models import Link, DownloaderEvent, ScraperEvent
from vidownloader.core.Worker import Scraper, Downloader
from vidownloader.core.Constants import EventType, WorkerType, Status
from vidownloader.core.Logger import get_logger
from vidownloader.core.VSettings import get_download_threads

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QTimer, QEventLoop


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
        self.lock = Lock()
        self.is_paused = False
    
    def run(self):
        logger.info("DownloadProcess started.")
        self._start_next_batch()

        loop = QEventLoop()
        while self.finished_threads < len(self.links):
            if self._stop_requested: return
            loop.processEvents()
            time.sleep(0.1)
        
        logger.info("DownloadProcess run method completed.")
        # Individual threads emit their own completion events with video_id
        # No need to emit a generic event here
        self.on_finish.emit("Download completed.", WorkerType.DOWNLOADER)

    def _start_next_batch(self):
        if self.is_paused:
            return
        
        with self.lock:
            max_threads = get_download_threads()
            while (self.active_threads < max_threads and
                    self.current_index < len(self.links)):
                
                if self._stop_requested: return
                
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
        if hasattr(self, 'downloader') and self.downloader:
            self.downloader = None
        super().stop()
    
    def pause(self):
        logger.info("Pausing all downloader threads.")
        with self.lock:
            self.is_paused = True
            # we'll let the running threads finish, but won't start new ones
            # TODO: implement better pausing mechanism
    
    def resume(self):
        logger.info("Resuming downloader threads.")
        with self.lock:
            self.is_paused = False
        # Call _start_next_batch OUTSIDE the lock to avoid deadlock
        self._start_next_batch()
    
    @pyqtSlot(DownloaderEvent)
    def event_handler(self, event: DownloaderEvent):
        # only handle completion or failure events to manage threads
        if event.event == EventType.STATUS and event.status in (Status.COMPLETED, Status.FAILED):
            
            with self.lock:
                self.finished_threads += 1
                self.active_threads -= 1
                self.update_progress.emit(self.finished_threads)
                
                for i, thread in enumerate(self.threads):
                    if not thread.isRunning():
                        self.threads.pop(i)
                        break
                
                if self.current_index < len(self.links):
                    QTimer.singleShot(0, self._start_next_batch)
            
        self._event.emit(event)
    