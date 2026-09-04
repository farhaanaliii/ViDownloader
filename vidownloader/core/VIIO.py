import json
from pathlib import Path
from typing import Union

from vidownloader.core.Models import Video


class VIIOError(Exception):
    pass


class InvalidFileError(VIIOError):
    pass


class VIIO:
    """
    ViDownloader I/O format for saving and loading video lists.

    File structure:
        [MAGIC: 4 bytes]["VIIO"]
        [VERSION: 1 byte]
        [PAYLOAD: XOR-encrypted JSON]
    """

    MAGIC = b"VIIO"
    VERSION = 1
    EXTENSION = ".viio"
    KEY = 0x15

    def __init__(self, filepath: Union[str, Path] = None):
        self.filepath = Path(filepath) if filepath else None

    def _apply_xor(self, payload: bytes) -> bytes:
        return bytes(b ^ self.KEY for b in payload)

    def _encode(self, videos: list[Video]) -> bytes:
        video_dicts = [v.to_dict() for v in videos]

        json_payload = json.dumps(video_dicts, ensure_ascii=False).encode("utf-8")
        encrypted_payload = self._apply_xor(json_payload)

        return self.MAGIC + bytes([self.VERSION]) + encrypted_payload

    def _decode(self, data: bytes) -> list[Video]:
        if len(data) < len(self.MAGIC) + 1:
            raise InvalidFileError("File too small to be a valid VIIO file")

        magic = data[: len(self.MAGIC)]
        if magic != self.MAGIC:
            raise InvalidFileError(f"Invalid file header. Expected {self.MAGIC!r}, got {magic!r}")

        version = data[len(self.MAGIC)]
        if version > self.VERSION:
            raise InvalidFileError(f"Unsupported file version {version}. Max supported: {self.VERSION}")

        encrypted_payload = data[len(self.MAGIC) + 1 :]
        json_payload = self._apply_xor(encrypted_payload)

        try:
            video_dicts = json.loads(json_payload.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise InvalidFileError(f"Corrupted file data: {e}")

        videos = []
        for video_dict in video_dicts:
            try:
                videos.append(Video.from_dict(video_dict))
            except (TypeError, KeyError) as e:
                raise InvalidFileError(f"Invalid video data in file: {e}")

        return videos

    def save(self, videos: list[Video], filepath: Union[str, Path] = None) -> Path:
        path = Path(filepath) if filepath else self.filepath

        if not path:
            raise VIIOError("No filepath provided for save operation")

        if path.suffix.lower() != self.EXTENSION:
            path = path.with_suffix(self.EXTENSION)

        path.parent.mkdir(parents=True, exist_ok=True)

        data = self._encode(videos)
        path.write_bytes(data)

        return path

    def load(self, filepath: Union[str, Path] = None) -> list[Video]:
        path = Path(filepath) if filepath else self.filepath

        if not path:
            raise VIIOError("No filepath provided for load operation")

        if not path.exists():
            raise FileNotFoundError(f"VIIO file not found: {path}")

        data = path.read_bytes()
        return self._decode(data)

    @classmethod
    def quick_save(cls, videos: list[Video], filepath: Union[str, Path]) -> Path:
        return cls().save(videos, filepath)

    @classmethod
    def quick_load(cls, filepath: Union[str, Path]) -> list[Video]:
        return cls().load(filepath)
