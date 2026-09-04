from dataclasses import asdict, dataclass
from pathlib import Path

from vidownloader.core.Constants import BridgeType, EventType, VideoType


@dataclass
class Link:
    url: str
    video_type: VideoType
    username: str = None
    video_id: str = None
    playlist_id: str = None
    playlist_name: str = None
    channel_id: str = None
    caption: str = None


@dataclass(kw_only=True)
class Video:
    no: int = 0
    caption: str
    percentage: str = "0%"
    status: str = "Pending"
    username: str
    video_id: str
    _type: VideoType
    url: str = None
    duration: str = None
    playlist_id: str = None
    playlist_name: str = None

    def __str__(self):
        return (
            f"Video(no={self.no}, caption='{self.caption}', percentage='{self.percentage}', "
            f"status='{self.status}', username='{self.username}', id='{self.video_id}', "
            f"url='{self.url}', type='{self._type}')"
        )

    def __repr__(self):
        return f"<Video #{self.no} - {self.caption} " f"[{self.status} - {self.percentage}]>"

    def to_dict(self):
        data = asdict(self)
        data["_type"] = self._type.value
        return data

    @classmethod
    def from_dict(cls, data: dict):
        data["_type"] = VideoType(data["_type"])
        return cls(**data)


@dataclass
class Bridge:
    bridge_type: BridgeType
    links: list[Link] = None
    exported: str = None
    videos: list[Video] = None


@dataclass
class DownloaderEvent:
    event: EventType
    video_id: int = None
    video_path: Path = None
    progress: str = None
    status: str = None


@dataclass
class ScraperEvent:
    event: EventType
    videos: list[Video] = None
    message: str = None
