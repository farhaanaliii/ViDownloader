"""
Unit tests for vidownloader.core.Utils module.
Tests URL parsing, filename sanitization, and utility functions.
"""

from pathlib import Path

import pytest

from vidownloader.core.Constants import VideoType
from vidownloader.core.Utils import (
    gen_uid,
    parse_links,
    sanitize_filename,
    truncate_text,
)


class TestParseLinks:
    """Tests for the parse_links function."""

    def test_parse_youtube_video_url(self):
        """Test parsing a standard YouTube video URL."""
        links = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        result = parse_links(links)

        assert len(result) == 1
        assert result[0].video_id == "dQw4w9WgXcQ"
        assert result[0].video_type == VideoType.VIDEO

    def test_parse_youtube_short_url(self):
        """Test parsing a YouTube Shorts URL."""
        links = "https://www.youtube.com/shorts/abcdefghijk"
        result = parse_links(links)

        assert len(result) == 1
        # Note: video_id is not extracted from shorts path, only from v= param
        assert result[0].video_type == VideoType.SHORT
        assert result[0].url == "https://www.youtube.com/shorts/abcdefghijk"

    def test_parse_youtube_channel_url(self):
        """Test parsing a YouTube channel URL."""
        links = "https://www.youtube.com/@farhaanaliii/videos"
        result = parse_links(links)

        assert len(result) == 1
        assert result[0].username == "farhaanaliii"

    def test_parse_youtu_be_url(self):
        """Test parsing a shortened youtu.be URL."""
        links = "https://youtu.be/dQw4w9WgXcQ"
        result = parse_links(links)

        assert len(result) == 1
        assert result[0].video_id == "dQw4w9WgXcQ"

    def test_parse_multiple_urls(self):
        """Test parsing multiple URLs."""
        links = """
        https://www.youtube.com/watch?v=video1id123
        https://www.youtube.com/shorts/short1id123
        https://www.youtube.com/@testuser/videos
        """
        result = parse_links(links)

        assert len(result) == 3

    def test_parse_empty_input(self):
        """Test parsing empty input."""
        result = parse_links("")
        assert result == []

    def test_parse_invalid_url(self):
        """Test parsing non-YouTube URL (should be ignored)."""
        links = "https://example.com/video"
        result = parse_links(links)

        assert result == []

    def test_parse_playlist_url(self):
        """Test parsing URL with playlist ID."""
        links = "https://www.youtube.com/watch?v=abc123def45&list=PLtest12345"
        result = parse_links(links)

        assert len(result) == 1
        assert result[0].playlist_id == "PLtest12345"
        assert result[0].video_id == "abc123def45"


class TestTruncateText:
    """Tests for the truncate_text function."""

    def test_short_text_unchanged(self):
        """Text shorter than width should remain unchanged."""
        result = truncate_text("Hello", 10)
        assert result == "Hello"

    def test_long_text_truncated(self):
        """Text longer than width should be truncated with ellipsis."""
        result = truncate_text("Hello World!", 8)
        assert result == "Hello..."
        assert len(result) == 8

    def test_exact_width(self):
        """Text exactly at width should remain unchanged."""
        result = truncate_text("Hello", 5)
        assert result == "Hello"

    def test_non_string_input(self):
        """Non-string input should return empty string."""
        result = truncate_text(None, 10)
        assert result == ""

        result = truncate_text(123, 10)
        assert result == ""


class TestGenUid:
    """Tests for the gen_uid function."""

    def test_default_length(self):
        """Default UID should be 20 characters."""
        result = gen_uid()
        assert len(result) == 20

    def test_custom_length(self):
        """Custom length UID generation."""
        result = gen_uid(10)
        assert len(result) == 10

    def test_uniqueness(self):
        """Generated UIDs should be unique."""
        uids = [gen_uid() for _ in range(100)]
        assert len(set(uids)) == 100

    def test_alphanumeric(self):
        """UID should only contain alphanumeric characters."""
        result = gen_uid()
        assert result.isalnum()


class TestSanitizeFilename:
    """Tests for the sanitize_filename function."""

    def test_removes_special_chars(self):
        """Special characters should be removed."""
        result = sanitize_filename("Test: Video / Name?")
        assert ":" not in result
        assert "/" not in result
        assert "?" not in result

    def test_preserves_spaces(self):
        """Single spaces should be preserved."""
        result = sanitize_filename("Test Video Name")
        assert result == "Test Video Name"

    def test_collapses_multiple_spaces(self):
        """Multiple spaces should be collapsed to single space."""
        result = sanitize_filename("Test   Video    Name")
        assert "  " not in result

    def test_strips_whitespace(self):
        """Leading/trailing whitespace should be removed."""
        result = sanitize_filename("  Test Video  ")
        assert result == "Test Video"

    def test_removes_windows_invalid_chars(self):
        """Windows invalid characters should be removed."""
        result = sanitize_filename('File<>:"|?*Name')
        assert "<" not in result
        assert ">" not in result
        assert "|" not in result
        assert "*" not in result

    def test_handles_unicode(self):
        """Unicode characters should be preserved."""
        result = sanitize_filename("Test 日本語 Video")
        assert "日本語" in result


class TestFormatDuration:
    """Tests for the format_duration function."""

    def test_format_seconds_only(self):
        """Test formatting duration less than a minute."""
        from vidownloader.core.Utils import format_duration

        result = format_duration(45)
        assert result == "0:45"

    def test_format_minutes_and_seconds(self):
        """Test formatting duration with minutes and seconds."""
        from vidownloader.core.Utils import format_duration

        result = format_duration(125)
        assert result == "2:05"

    def test_format_hours_minutes_seconds(self):
        """Test formatting duration with hours."""
        from vidownloader.core.Utils import format_duration

        result = format_duration(3665)
        assert result == "1:01:05"

    def test_format_zero_duration(self):
        """Test formatting zero duration."""
        from vidownloader.core.Utils import format_duration

        result = format_duration(0)
        assert result == "0:00"

    def test_format_exact_minute(self):
        """Test formatting exact minute duration."""
        from vidownloader.core.Utils import format_duration

        result = format_duration(60)
        assert result == "1:00"


class TestFormatSize:
    """Tests for the format_size function."""

    def test_format_bytes(self):
        """Test formatting bytes."""
        from vidownloader.core.Utils import format_size

        result = format_size(500)
        assert "B" in result

    def test_format_kilobytes(self):
        """Test formatting kilobytes."""
        from vidownloader.core.Utils import format_size

        result = format_size(1024 * 5)
        assert "KB" in result or "KiB" in result

    def test_format_megabytes(self):
        """Test formatting megabytes."""
        from vidownloader.core.Utils import format_size

        result = format_size(1024 * 1024 * 10)
        assert "MB" in result or "MiB" in result

    def test_format_gigabytes(self):
        """Test formatting gigabytes."""
        from vidownloader.core.Utils import format_size

        result = format_size(1024 * 1024 * 1024 * 2)
        assert "GB" in result or "GiB" in result

    def test_format_zero_size(self):
        """Test formatting zero size."""
        from vidownloader.core.Utils import format_size

        result = format_size(0)
        assert "0" in result


class TestBuildDownloadPath:
    """Tests for the build_download_path function."""

    def test_build_path_for_single_video(self):
        """Test building path for a single video."""
        from vidownloader.core.Models import Link
        from vidownloader.core.Utils import build_download_path

        link = Link(
            url="https://www.youtube.com/watch?v=test123",
            video_type=VideoType.VIDEO,
            username="testuser",
            video_id="test123",
        )

        path = build_download_path(link)
        assert isinstance(path, Path)

    def test_build_path_for_playlist(self):
        """Test building path for playlist video."""
        from vidownloader.core.Models import Link
        from vidownloader.core.Utils import build_download_path

        link = Link(
            url="https://www.youtube.com/watch?v=test123",
            video_type=VideoType.VIDEO,
            username="testuser",
            video_id="test123",
            playlist_id="PLtest123",
            playlist_name="Test Playlist",
        )

        path = build_download_path(link)
        assert isinstance(path, Path)


class TestGenerateExportFilename:
    """Tests for the generate_export_filename function."""

    def test_generates_unique_filename(self):
        """Test that export filenames are unique."""
        import time

        from vidownloader.core.Utils import generate_export_filename

        filename1 = generate_export_filename()
        time.sleep(1.1)  # Wait to ensure different timestamp
        filename2 = generate_export_filename()

        assert filename1 != filename2

    def test_filename_format(self):
        """Test export filename format."""
        from vidownloader.core.Utils import generate_export_filename

        filename = generate_export_filename()
        assert "export" in filename.lower() or "vidownloader" in filename.lower()
