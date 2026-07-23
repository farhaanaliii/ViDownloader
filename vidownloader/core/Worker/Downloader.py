import traceback
from pathlib import Path

from PySide6.QtCore import QThread, Signal
from yt_dlp import YoutubeDL

from vidownloader.core.Constants import EventType, Status
from vidownloader.core.Logger import get_logger
from vidownloader.core.Models import DownloaderEvent, Link
from vidownloader.core.Utils import build_download_path, build_filename

logger = get_logger("Downloader")


class Downloader(QThread):
    _event = Signal(DownloaderEvent)

    def __init__(self, link: Link):
        super().__init__()
        self.link = link

    def run(self):
        logger.debug(f"Starting download for: {self.link.url}")
        self.emit_status(Status.STARTING)

        dl_path = build_download_path(self.link)
        file_name = build_filename(self.link, dl_path)
        file_path = dl_path / file_name

        self._download(file_path)

    def _download(
        self, file_path: Path, retries: int = 3
    ) -> bool:  # TODO: Make retries configurable
        logger.debug(f"Downloading to: {file_path}")

        ydl_opts = {
            "format": "bv*+ba/b",  # TODO: Make format configurable
            "outtmpl": file_path.__fspath__(),
            "merge_output_format": "mp4",  # TODO: Make format configurable
            "progress_hooks": [self._progress_hook],
            "quiet": True,
            "no_warnings": True,
            "noprogress": True,
            "retries": 10,
            "fragment_retries": 10,
            "continuedl": True,
            #'cookiesfrombrowser': 'chrome' # TODO: Add browser cookie support later
        }

        for attempt in range(retries + 1):
            try:
                self.emit_status(Status.DOWNLOADING)
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([self.link.url])

                self.emit_progress("100%")
                self.emit_status(Status.COMPLETED, file_path)
                return True

            except Exception as e:
                logger.warning(
                    f"Download attempt {attempt + 1}/{retries + 1} failed: {e}"
                )
                logger.debug(traceback.format_exc())

                if attempt < retries:
                    logger.info(f"Retrying download...")
                    self.emit_status(Status.RETRYING)
                    continue

                logger.error(f"Download failed after {retries + 1} attempts")
                self.emit_status(Status.FAILED)
                return False

    def emit_progress(self, progress: str):
        self._event.emit(
            DownloaderEvent(
                event=EventType.PROGRESS, progress=progress, video_id=self.link.video_id
            )
        )

    def emit_status(self, status: Status, video_path: Path = None):
        self._event.emit(
            DownloaderEvent(
                event=EventType.STATUS,
                status=status,
                video_id=self.link.video_id,
                video_path=video_path,
            )
        )

    def _progress_hook(self, d: dict):
        if d["status"] == "downloading":
            total_bytes = d.get("total_bytes") or d.get("total_bytes_estimate")
            if total_bytes:
                percent = d["downloaded_bytes"] / total_bytes * 100
                self.emit_progress(f"{percent:.2f}%")
        elif d["status"] == "finished":
            self.emit_progress("100%")
