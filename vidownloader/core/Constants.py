import os
import platform
import re
from enum import IntEnum
from pathlib import Path

# StrEnum is available in Python 3.11 and later
# Fallback for earlier versions
try:
    from enum import StrEnum as StringEnum
except ImportError:
    from enum import Enum

    class StringEnum(str, Enum):
        pass


from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class Author:
    GITHUB = "farhaanaliii"
    NAME = "Farhan Ali"
    GITHUB_URL = f"https://github.com/{GITHUB}/ViDownloader"


class App:
    NAME = "ViDownloader"
    VERSION = "0.5.0"
    ICON = "icon.png"
    USER_AGENT = f"{NAME}/{VERSION} - {Author.GITHUB_URL}"


class YouTube:
    API = "https://www.youtube.com/youtubei/v1"
    KEY = "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
    VIDEOS_PARAMS = "EgZ2aWRlb3PyBgQKAjoA"
    SHORTS_PARAMS = "EgZzaG9ydHPyBgUKA5oBAA%3D%3D"


class Paths:
    if platform.system() == "Windows":
        BASE = Path(os.getenv("LOCALAPPDATA")) / App.NAME
    else:
        BASE = Path.home() / ".config" / App.NAME
    DATA = BASE / "data"
    LOGS = BASE / "logs"

    @staticmethod
    def ensure_paths():
        Paths.BASE.mkdir(parents=True, exist_ok=True)
        Paths.DATA.mkdir(exist_ok=True)
        Paths.LOGS.mkdir(exist_ok=True)


class BridgeType(IntEnum):
    LINKS = 1
    IMPORTED = 2


class WorkerType(IntEnum):
    SCRAPER = 1
    DOWNLOADER = 2


class EventType(IntEnum):
    PROGRESS = 1
    STATUS = 2
    VIDEOS = 3
    MESSAGE = 4


class VideoType(StringEnum):
    VIDEO = "videos"
    SHORT = "shorts"


class TreeViewColumns(IntEnum):
    NO = 0
    CAPTION = 1
    PROGRESS = 2
    STATUS = 3
    USERNAME = 4
    ID = 5
    SIZE = 6
    DURATION = 7


class TreeViewRoles(IntEnum):
    VIDEO_DATA = Qt.UserRole + 1
    VIDEO_PATH = Qt.UserRole + 2


class StatusColors:
    SUCCESS = QColor(46, 204, 113, 100)
    "#2ECC71"
    ERROR = QColor(231, 76, 60, 120)
    "#E74C3C"
    WARNING = QColor(241, 196, 15, 110)
    "#F1C40F"
    INFO = QColor(52, 152, 219, 100)
    "#3498DB"
    PENDING = QColor(149, 165, 166, 90)
    "#95A5A6"


class Status(StringEnum):
    STARTING = "Starting"
    PENDING = "Pending"
    DOWNLOADING = "Downloading"
    COMPLETED = "Completed"
    RETRYING = "Retrying"
    FAILED = "Failed"
    SKIPPED = "Skipped"


class FileName(IntEnum):
    CAPTION = 1
    VIDEO_ID = 2
    RANDOM = 3


class PlaylistOrganization(IntEnum):
    BY_PLAYLIST = 0
    BY_UPLOADER = 1


class SingleVideoOrganization(IntEnum):
    GROUP_SINGLES = 0
    BY_UPLOADER = 1


class VideoQuality(StringEnum):
    BEST = "bv*+ba/b"
    P2160 = "bv*[height<=2160]+ba/bv*[width<=2160]+ba/b"
    P1440 = "bv*[height<=1440]+ba/bv*[width<=1440]+ba/b"
    P1080 = "bv*[height<=1080]+ba/bv*[width<=1080]+ba/b"
    P720 = "bv*[height<=720]+ba/bv*[width<=720]+ba/b"
    P480 = "bv*[height<=480]+ba/bv*[width<=480]+ba/b"
    P360 = "bv*[height<=360]+ba/bv*[width<=360]+ba/b"
    P240 = "bv*[height<=240]+ba/bv*[width<=240]+ba/b"
    P144 = "bv*[height<=144]+ba/bv*[width<=144]+ba/b"
    AUDIO_ONLY = "ba/b"


class OutputFormat(StringEnum):
    MP4 = "mp4"
    MKV = "mkv"
    WEBM = "webm"


DISALLOWED_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1F]')
