from pathlib import Path
from typing import Any, Optional, Type

from vidownloader.core.Constants import App, Author, FileName

from PyQt5.QtCore import QSettings


class VSettings:
    VERSION = "v1"
    
    def __init__(self) -> None:
        self._settings = QSettings(Author.NAME, App.NAME)

    def _key(self, key: str) -> str:
        return f"{self.VERSION}/{key}"
    
    def get_value(self, key: str, default: Optional[Any] = None, value_type: Optional[Type] = None) -> Any:
        key = self._key(key)
        value = self._settings.value(key, default)
        if value_type is not None and value is not None:
            try:
                return value_type(value)
            except (ValueError, TypeError):
                return default
        return value


    def set_value(self, key: str, value: Any) -> None:
        self._settings.setValue(self._key(key), value)

    def remove(self, key: str) -> None:
        self._settings.remove(self._key(key))

    def contains(self, key: str) -> bool:
        return self._settings.contains(self._key(key))

    def clear_all(self) -> None:
        self._settings.clear()

    def get_download_location(self) -> str:
        return self.get_value(
            "download/location",
            str((Path("~").expanduser() / "Downloads" / App.NAME).absolute()),
            str
        )
    
    def set_download_location(self, location: str) -> None:
        self.set_value("download/location", location)
    
    def get_export_location(self) -> str:
        return self.get_value(
            "export/location",
            str((Path("~").expanduser() / "Documents" / App.NAME).absolute()),
            str
        )
    
    def set_export_location(self, location: str) -> None:
        self.set_value("export/location", location)
    
    def get_file_naming_mode(self) -> FileName:
        value = self.get_value("file/naming_mode", FileName.CAPTION.value, int)
        
        try:
            return FileName(value)
        except ValueError:
            return FileName.CAPTION

    def set_file_naming_mode(self, mode: FileName) -> None:
        self.set_value("file/naming_mode", mode.value)
    
    def get_download_threads(self) -> int:
        return self.get_value("download/threads", 4, int)

    def set_download_threads(self, threads: int) -> None:
        self.set_value("download/threads", threads)

settings = VSettings()

get_download_location = settings.get_download_location
set_download_location = settings.set_download_location

get_export_location = settings.get_export_location
set_export_location = settings.set_export_location

get_file_naming_mode = settings.get_file_naming_mode
set_file_naming_mode = settings.set_file_naming_mode

get_download_threads = settings.get_download_threads
set_download_threads = settings.set_download_threads
