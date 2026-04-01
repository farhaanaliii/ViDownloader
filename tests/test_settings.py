"""
Unit tests for vidownloader.core.VSettings module.
Tests settings storage, retrieval, and default values.
"""

from unittest.mock import Mock, patch

import pytest

from vidownloader.core.Constants import FileName
from vidownloader.core.VSettings import VSettings


class TestVSettings:
    """Tests for the VSettings class."""

    @pytest.fixture
    def settings(self):
        """Create a fresh VSettings instance for each test."""
        return VSettings()

    def test_initialization(self, settings):
        """Test VSettings initialization."""
        assert settings.VERSION == "v1"
        assert settings._settings is not None

    def test_key_versioning(self, settings):
        """Test that keys are versioned."""
        key = settings._key("test_key")
        assert key.startswith(settings.VERSION + "/")
        assert "test_key" in key

    @patch("vidownloader.core.VSettings.QSettings")
    def test_get_value_returns_stored_value(self, mock_qsettings):
        """Test getting a stored value."""
        mock_instance = Mock()
        mock_instance.value.return_value = "stored_value"
        mock_qsettings.return_value = mock_instance

        settings = VSettings()
        value = settings.get_value("test_key")

        assert value == "stored_value"

    @patch("vidownloader.core.VSettings.QSettings")
    def test_get_value_with_default(self, mock_qsettings):
        """Test getting value with default when not set."""
        mock_instance = Mock()
        mock_instance.value.return_value = None
        mock_qsettings.return_value = mock_instance

        settings = VSettings()
        value = settings.get_value("test_key", default="default_value")

        assert value is None or value == "default_value"

    @patch("vidownloader.core.VSettings.QSettings")
    def test_get_value_with_type_conversion(self, mock_qsettings):
        """Test getting value with type conversion."""
        mock_instance = Mock()
        mock_instance.value.return_value = "42"
        mock_qsettings.return_value = mock_instance

        settings = VSettings()
        value = settings.get_value("test_key", value_type=int)

        assert value == 42
        assert isinstance(value, int)

    @patch("vidownloader.core.VSettings.QSettings")
    def test_get_value_type_conversion_failure(self, mock_qsettings):
        """Test that type conversion failure returns default."""
        mock_instance = Mock()
        mock_instance.value.return_value = "not_a_number"
        mock_qsettings.return_value = mock_instance

        settings = VSettings()
        value = settings.get_value("test_key", default=0, value_type=int)

        assert value == 0

    @patch("vidownloader.core.VSettings.QSettings")
    def test_set_value(self, mock_qsettings):
        """Test setting a value."""
        mock_instance = Mock()
        mock_qsettings.return_value = mock_instance

        settings = VSettings()
        settings.set_value("test_key", "test_value")

        mock_instance.setValue.assert_called_once()

    @patch("vidownloader.core.VSettings.QSettings")
    def test_remove_key(self, mock_qsettings):
        """Test removing a key."""
        mock_instance = Mock()
        mock_qsettings.return_value = mock_instance

        settings = VSettings()
        settings.remove("test_key")

        mock_instance.remove.assert_called_once()

    @patch("vidownloader.core.VSettings.QSettings")
    def test_contains_key(self, mock_qsettings):
        """Test checking if key exists."""
        mock_instance = Mock()
        mock_instance.contains.return_value = True
        mock_qsettings.return_value = mock_instance

        settings = VSettings()
        result = settings.contains("test_key")

        assert result is True

    @patch("vidownloader.core.VSettings.QSettings")
    def test_clear_all(self, mock_qsettings):
        """Test clearing all settings."""
        mock_instance = Mock()
        mock_qsettings.return_value = mock_instance

        settings = VSettings()
        settings.clear_all()

        mock_instance.clear.assert_called_once()

    @patch("vidownloader.core.VSettings.QSettings")
    def test_get_download_location_default(self, mock_qsettings):
        """Test getting default download location."""
        mock_instance = Mock()

        # Mock to return the default path
        from pathlib import Path

        default_path = str(
            (Path("~").expanduser() / "Downloads" / "ViDownloader").absolute()
        )
        mock_instance.value.return_value = default_path
        mock_qsettings.return_value = mock_instance

        settings = VSettings()
        location = settings.get_download_location()

        assert "ViDownloader" in location
        assert isinstance(location, str)

    @patch("vidownloader.core.VSettings.QSettings")
    def test_set_download_location(self, mock_qsettings):
        """Test setting download location."""
        mock_instance = Mock()
        mock_qsettings.return_value = mock_instance

        settings = VSettings()
        settings.set_download_location("/test/path")

        mock_instance.setValue.assert_called_once()

    @patch("vidownloader.core.VSettings.QSettings")
    def test_get_export_location_default(self, mock_qsettings):
        """Test getting default export location."""
        mock_instance = Mock()

        # Mock to return the default path
        from pathlib import Path

        default_path = str(
            (Path("~").expanduser() / "Documents" / "ViDownloader").absolute()
        )
        mock_instance.value.return_value = default_path
        mock_qsettings.return_value = mock_instance

        settings = VSettings()
        location = settings.get_export_location()

        assert "ViDownloader" in location
        assert isinstance(location, str)

    @patch("vidownloader.core.VSettings.QSettings")
    def test_get_file_naming_mode_default(self, mock_qsettings):
        """Test getting default file naming mode."""
        mock_instance = Mock()
        mock_instance.value.return_value = None
        mock_qsettings.return_value = mock_instance

        settings = VSettings()
        mode = settings.get_file_naming_mode()

        assert mode == FileName.CAPTION

    @patch("vidownloader.core.VSettings.QSettings")
    def test_set_file_naming_mode(self, mock_qsettings):
        """Test setting file naming mode."""
        mock_instance = Mock()
        mock_qsettings.return_value = mock_instance

        settings = VSettings()
        settings.set_file_naming_mode(FileName.VIDEO_ID)

        mock_instance.setValue.assert_called_once()

    @patch("vidownloader.core.VSettings.QSettings")
    def test_get_download_threads_default(self, mock_qsettings):
        """Test getting default download threads."""
        mock_instance = Mock()
        # Mock to return the default value
        mock_instance.value.return_value = 4
        mock_qsettings.return_value = mock_instance

        settings = VSettings()
        threads = settings.get_download_threads()

        assert threads == 4

    @patch("vidownloader.core.VSettings.QSettings")
    def test_set_download_threads(self, mock_qsettings):
        """Test setting download threads."""
        mock_instance = Mock()
        mock_qsettings.return_value = mock_instance

        settings = VSettings()
        settings.set_download_threads(8)

        mock_instance.setValue.assert_called_once()

    @patch("vidownloader.core.VSettings.QSettings")
    def test_get_playlist_organization_default(self, mock_qsettings):
        """Test getting default playlist organization."""
        mock_instance = Mock()
        mock_instance.value.return_value = None
        mock_qsettings.return_value = mock_instance

        settings = VSettings()
        org = settings.get_playlist_organization()

        from vidownloader.core.Constants import PlaylistOrganization

        assert org == PlaylistOrganization.BY_PLAYLIST

    @patch("vidownloader.core.VSettings.QSettings")
    def test_set_playlist_organization(self, mock_qsettings):
        """Test setting playlist organization."""
        from vidownloader.core.Constants import PlaylistOrganization

        mock_instance = Mock()
        mock_qsettings.return_value = mock_instance

        settings = VSettings()
        settings.set_playlist_organization(PlaylistOrganization.BY_UPLOADER)

        mock_instance.setValue.assert_called_once()

    @patch("vidownloader.core.VSettings.QSettings")
    def test_get_single_video_organization_default(self, mock_qsettings):
        """Test getting default single video organization."""
        mock_instance = Mock()
        mock_instance.value.return_value = None
        mock_qsettings.return_value = mock_instance

        settings = VSettings()
        org = settings.get_single_video_organization()

        from vidownloader.core.Constants import SingleVideoOrganization

        assert org == SingleVideoOrganization.GROUP_SINGLES

    @patch("vidownloader.core.VSettings.QSettings")
    def test_set_single_video_organization(self, mock_qsettings):
        """Test setting single video organization."""
        from vidownloader.core.Constants import SingleVideoOrganization

        mock_instance = Mock()
        mock_qsettings.return_value = mock_instance

        settings = VSettings()
        settings.set_single_video_organization(SingleVideoOrganization.BY_UPLOADER)

        mock_instance.setValue.assert_called_once()

    @patch("vidownloader.core.VSettings.QSettings")
    def test_file_naming_mode_invalid_value(self, mock_qsettings):
        """Test that invalid file naming mode value returns default."""
        mock_instance = Mock()
        mock_instance.value.return_value = 999
        mock_qsettings.return_value = mock_instance

        settings = VSettings()
        mode = settings.get_file_naming_mode()

        assert mode == FileName.CAPTION
