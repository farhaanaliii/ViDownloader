import ctypes
import os
import platform
import random
import re
import string
import sys
import traceback
import subprocess
from datetime import datetime
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem

from vidownloader.core import Logger, VSettings
from vidownloader.core.Constants import (
    DISALLOWED_CHARS,
    App,
    FileName,
    PlaylistOrganization,
    SingleVideoOrganization,
    TreeViewColumns,
    TreeViewRoles,
    VideoType,
)
from vidownloader.core.Models import Link, Video
from vidownloader.core.VIIO import VIIO

logger = Logger.get_logger("Utils")


if platform.system() == "Windows":
    import winreg


def parse_links(links: str) -> list[Link]:
    """
    Parses a list of link strings into Link objects with extracted username and video ID/UID.

    Args:
        links (list[str]): A list of link strings.

    Returns:
        list[Link]: A list of Link objects.
    """

    links = [link.strip() for link in links.splitlines() if link.strip()]
    if not links:
        return []

    parsed_links = []

    for link in links:
        username = None
        video_id = None
        playlist_id = None
        channel_id = None
        video_type = VideoType.VIDEO

        if "youtube.com" in link or "youtu.be" in link:
            video_match = re.search(
                r"(?:v=|youtu\.be/|shorts/)([0-9A-Za-z_-]{11})", link
            )
            video_id = video_match.group(1) if video_match else None

            user_match = re.search(r"youtube\.com/@([A-Za-z0-9._-]+)", link)
            username = user_match.group(1) if user_match else None

            playlist_match = re.search(r"[?&]list=([A-Za-z0-9_-]+)", link)
            playlist_id = playlist_match.group(1) if playlist_match else None
            
            # since user pasted a video link, we don't need to treat it as a playlist link
            # ig we'll need to make this better
            if video_id and playlist_id:
                playlist_id = None

            channel_match = re.search(r"(?:channel/)(UC[0-9A-Za-z_-]+)", link)
            channel_id = channel_match.group(1) if channel_match else None

            if "/shorts" in link:
                video_type = VideoType.SHORT

        else:
            continue

        parsed_links.append(
            Link(
                video_type=video_type,
                url=link,
                username=username,
                video_id=video_id,
                playlist_id=playlist_id,
                channel_id=channel_id,
            )
        )

    return parsed_links


def truncate_text(text: str, width: int) -> str:
    """Truncate text with ellipsis if it exceeds width."""
    if not isinstance(text, str):
        return ""
    return text if len(text) <= width else text[: width - 3] + "..."


def format_duration(seconds: int) -> str:
    """Format duration in seconds to HH:MM:SS or MM:SS format."""
    if seconds is None or seconds < 0:
        return ""

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"


def treeitem_to_link(item: QTreeWidgetItem) -> Link:
    """
    Convert a QTreeWidgetItem row into a Link object.
    """
    username = item.text(TreeViewColumns.USERNAME)
    video_id = item.text(TreeViewColumns.ID)

    # The visible caption is truncated, so a tooltip is used to display the full text.
    # The tooltip is set when the item is created.
    caption = item.toolTip(TreeViewColumns.CAPTION)
    user_data = item.data(TreeViewColumns.NO, TreeViewRoles.VIDEO_DATA)
    vtype: VideoType = user_data[0]
    url: str = user_data[1]
    playlist_id: str = user_data[2] if len(user_data) > 2 else None
    playlist_name: str = user_data[3] if len(user_data) > 3 else None

    return Link(
        url=url,
        video_type=vtype,
        username=username,
        video_id=video_id,
        caption=caption,
        playlist_id=playlist_id,
        playlist_name=playlist_name,
    )


def video_to_treeitem(video: Video) -> QTreeWidgetItem:
    item = QTreeWidgetItem(
        [
            str(video.no),
            truncate_text(video.caption, 50),
            video.percentage,
            video.status,
            video.username,
            video.video_id,
            "",
            format_duration(video.duration),
        ]
    )

    # Store playlist metadata along with video type and url
    item.setData(
        TreeViewColumns.NO,
        TreeViewRoles.VIDEO_DATA,
        (video._type, video.url, video.playlist_id, video.playlist_name),
    )
    item.setToolTip(TreeViewColumns.CAPTION, video.caption)
    return item


def treeitem_to_video(item: QTreeWidgetItem) -> Video:
    """
    Convert a QTreeWidgetItem row back into a Video object.
    """
    video_data: tuple = item.data(TreeViewColumns.NO, TreeViewRoles.VIDEO_DATA)
    vtype: VideoType = video_data[0]
    video_url: str = video_data[1]
    
    # Get full caption from tooltip (visible text is truncated)
    caption = item.toolTip(TreeViewColumns.CAPTION)
    if not caption:
        caption = item.text(TreeViewColumns.CAPTION)

    try:
        no = int(item.text(TreeViewColumns.NO))
    except (ValueError, TypeError):
        no = 0

    # Parse duration from formatted string (MM:SS or HH:MM:SS)
    duration_str = item.text(TreeViewColumns.DURATION)
    duration = None
    if duration_str:
        try:
            parts = duration_str.split(":")
            if len(parts) == 2:  # MM:SS
                duration = int(parts[0]) * 60 + int(parts[1])
            elif len(parts) == 3:  # HH:MM:SS
                duration = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        except (ValueError, IndexError):
            duration = None

    return Video(
        no=no,
        caption=caption,
        percentage=item.text(TreeViewColumns.PROGRESS),
        status=item.text(TreeViewColumns.STATUS),
        username=item.text(TreeViewColumns.USERNAME),
        video_id=item.text(TreeViewColumns.ID),
        _type=vtype,
        url=video_url,
        duration=duration,
    )


def build_download_path(link: Link) -> Path:
    """
    Build the download path for a given Link object.
    Organization depends on link type and user settings.
    """

    base_path = Path(VSettings.get_download_location())

    if link.playlist_id:
        playlist_org = VSettings.get_playlist_organization()

        if playlist_org == PlaylistOrganization.BY_PLAYLIST:
            playlist_name = link.playlist_name or link.playlist_id
            playlist_name = sanitize_filename(playlist_name)
            path = base_path / "playlists" / playlist_name
        else:
            path = base_path / link.username

    elif not link.channel_id:
        single_org = VSettings.get_single_video_organization()

        if single_org == SingleVideoOrganization.GROUP_SINGLES:
            path = base_path / "direct_videos"
        else:
            path = base_path / link.username

    else:
        path = base_path / link.username

    path.mkdir(parents=True, exist_ok=True)
    return path


def build_filename(link: Link, dl_path: Path) -> str:
    file_name_type = VSettings.get_file_naming_mode()

    if file_name_type == FileName.VIDEO_ID:
        return f"{link.video_id}.mp4"
    elif file_name_type == FileName.CAPTION:
        cleaned_caption = sanitize_filename(link.caption, dl_path)
        return f"{cleaned_caption}.mp4"
    else:
        return f"{gen_uid()}.mp4"


def get_system_drive():
    return os.environ.get("SYSTEMDRIVE", "C:").strip().upper().rstrip("\\/")


def get_max_filename_length(root_path: Path) -> int:
    """
    Returns the maximum filename length for a given drive.

    Modern Windows (10/11) with long path support can exceed 260 characters.
    This function checks if long paths are enabled via the registry and returns
    the correct limit when possible. For most practical use cases, 260 is fine
    — just note it's a legacy limit.
    """

    if platform.system() != "Windows":
        try:
            return os.pathconf(root_path, "PC_NAME_MAX")
        except Exception as e:
            logger.warning(
                f"Failed to get PC_NAME_MAX for {os.path.abspath(root_path)}: {e}"
            )
            return 255  # Default for most Unix-like filesystems

    try:

        def is_long_path_enabled() -> bool:
            try:
                with winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SYSTEM\CurrentControlSet\Control\FileSystem",
                ) as key:
                    value, _ = winreg.QueryValueEx(key, "LongPathsEnabled")
                    return value == 1
            except Exception:
                return False

        drive_letter = root_path.drive.upper().rstrip("\\/")

        if not drive_letter.endswith(":"):
            drive_letter += ":"

        volume_name_buffer = ctypes.create_unicode_buffer(1024)
        file_system_name_buffer = ctypes.create_unicode_buffer(1024)
        max_component_length = ctypes.c_uint32()
        file_system_flags = ctypes.c_uint32()

        result = ctypes.windll.kernel32.GetVolumeInformationW(
            ctypes.c_wchar_p(f"{drive_letter}\\"),
            volume_name_buffer,
            ctypes.sizeof(volume_name_buffer),
            None,
            ctypes.byref(max_component_length),
            ctypes.byref(file_system_flags),
            file_system_name_buffer,
            ctypes.sizeof(file_system_name_buffer),
        )

        if result:
            # Check if Windows long path support is active
            if is_long_path_enabled():
                return 32767
            return max_component_length.value

        return 255

    except Exception as e:
        logger.warning(f"Error getting max filename length: {e}")
        logger.debug(traceback.format_exc())
        return 255


def gen_uid(length=20):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def sanitize_filename(text: str, path: Path = Path()) -> str:
    try:
        safe_text = re.sub(DISALLOWED_CHARS, "", text.strip())
        safe_text = re.sub(r"\s+", " ", safe_text).strip()

        max_len = (
            get_max_filename_length(path) - len(str(path)) - 11
        )  # Reserve space for suffix

        return safe_text[: max(max_len, 1)]

    except Exception as e:
        logger.warning(f"Sanitization error: {e}")
        logger.debug(traceback.format_exc())
        return gen_uid(10)


def validate_file_path(file_path: Path) -> bool:
    try:
        dir_path = file_path.parent
        if dir_path:
            dir_path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.warning(f"Path validation error: {e}")
        logger.debug(traceback.format_exc())
        return False


def filter_string(text: str, path: Path = Path()) -> str:
    base_name = sanitize_filename(text, path)
    full_path = path / base_name
    _rand = f"#{random.randint(111, 999)}"

    if not validate_file_path(full_path):
        return f"{gen_uid()} {_rand}"

    if len(full_path) > get_max_filename_length():
        base_name = base_name[: get_max_filename_length() - len(path) - 11]

    return f"{base_name} {_rand}"


def load_fonts():
    """Load application fonts from Qt resources"""

    font_resources = [
        ":/fonts/Poppins-Regular.ttf",
        ":/fonts/Poppins-Medium.ttf",
        ":/fonts/Poppins-SemiBold.ttf",
    ]

    for font_path in font_resources:
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            logger.warning(f"Failed to load font: {font_path}")
        else:
            families = QFontDatabase.applicationFontFamilies(font_id)
            logger.info(f"Loaded font: {families}")


def is_frozen():
    """Check if running as bundled executable (PyInstaller/Nuitka)"""
    return getattr(sys, "frozen", False) or hasattr(sys, "_MEIPASS")


def exception_hook(exctype, value, tb):
    """Global exception handler for uncaught exceptions"""

    exception_text = "".join(traceback.format_exception(exctype, value, tb))
    logger.error(f"Uncaught exception: {exctype.__name__}: {value}")
    logger.debug(exception_text)

    # Only skip these exceptions during development
    if not is_frozen() and exctype in [PermissionError, KeyboardInterrupt]:
        return

    msg_box = QMessageBox()
    msg_box.setWindowTitle("Application Error")
    msg_box.setText(f"An unexpected error occurred: {exctype.__name__}")
    msg_box.setInformativeText(
        "Please copy the error details and report to the developer."
    )
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setDetailedText(exception_text)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec()


def generate_export_filename() -> str:
    """Generate a default filename for exporting videos."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{App.NAME}_exports_{timestamp}{VIIO.EXTENSION}"


def format_size(size_bytes: int) -> str:
    """Format size in bytes to human-readable"""
    for unit in ("B", "KB", "MB", "GB"):
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} GB"

def play_video(video_path: str):
    system = platform.system()
    
    if system == "Windows":
        cmd = ["cmd", "/c", "start", "", video_path]
    elif system == "Linux":
        cmd = ["xdg-open", video_path]
    elif system == "Darwin":  # macOS
        cmd = ["open", video_path]
    else:
        logger.warning(f"Unsupported platform for playing video: {platform.system()}")
        return
    
    subprocess.run(cmd, check=True)

