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


from PyQt5.QtGui import QColor


class Author:
    GITHUB = "farhaanaliii"
    NAME = "Farhan Ali"
    GITHUB_URL = f"https://github.com/{GITHUB}/ViDownloader"


class App:
    NAME = "ViDownloader"
    VERSION = "1.0.0-beta2"
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
    SELECT = 0
    NO = 1
    CAPTION = 2
    PROGRESS = 3
    STATUS = 4
    USERNAME = 5
    ID = 6
    SIZE = 7
    DURATION = 8


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


DISALLOWED_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1F]')
