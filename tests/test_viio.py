"""
Unit tests for vidownloader.core.VIIO module.
Tests file I/O, encryption, and error handling.
"""

import tempfile
from pathlib import Path

import pytest

from vidownloader.core.Constants import VideoType
from vidownloader.core.Models import Video
from vidownloader.core.VIIO import VIIO, InvalidFileError, VIIOError


class TestVIIO:
    """Tests for the VIIO class."""

    @pytest.fixture
    def sample_videos(self):
        """Sample videos for testing."""
        return [
            Video(
                no=1,
                caption="Test Video 1",
                username="testuser",
                video_id="video1",
                _type=VideoType.VIDEO,
                url="https://www.youtube.com/watch?v=video1",
                duration=120,
            ),
            Video(
                no=2,
                caption="Test Short 1",
                username="testuser",
                video_id="short1",
                _type=VideoType.SHORT,
                url="https://www.youtube.com/shorts/short1",
                duration=30,
            ),
        ]

    @pytest.fixture
    def temp_file(self):
        """Create a temporary file for testing."""
        with tempfile.NamedTemporaryFile(suffix=".viio", delete=False) as f:
            temp_path = Path(f.name)
        yield temp_path
        if temp_path.exists():
            temp_path.unlink()

    def test_viio_initialization(self):
        """Test VIIO initialization."""
        viio = VIIO()
        assert viio.filepath is None

        filepath = Path("test.viio")
        viio = VIIO(filepath)
        assert viio.filepath == filepath

    def test_xor_encryption_reversible(self):
        """Test that XOR encryption is reversible."""
        viio = VIIO()
        original = b"Hello, World!"

        encrypted = viio._apply_xor(original)
        decrypted = viio._apply_xor(encrypted)

        assert original == decrypted
        assert original != encrypted

    def test_encode_videos(self, sample_videos):
        """Test encoding videos to bytes."""
        viio = VIIO()
        encoded = viio._encode(sample_videos)

        assert isinstance(encoded, bytes)
        assert encoded.startswith(VIIO.MAGIC)
        assert encoded[len(VIIO.MAGIC)] == VIIO.VERSION

    def test_decode_videos(self, sample_videos):
        """Test decoding videos from bytes."""
        viio = VIIO()
        encoded = viio._encode(sample_videos)
        decoded = viio._decode(encoded)

        assert len(decoded) == len(sample_videos)
        assert decoded[0].caption == sample_videos[0].caption
        assert decoded[0].video_id == sample_videos[0].video_id
        assert decoded[1]._type == sample_videos[1]._type

    def test_save_and_load(self, sample_videos, temp_file):
        """Test saving and loading videos."""
        viio = VIIO(temp_file)

        saved_path = viio.save(sample_videos)
        assert saved_path.exists()
        assert saved_path.suffix == ".viio"

        loaded_videos = viio.load()
        assert len(loaded_videos) == len(sample_videos)
        assert loaded_videos[0].caption == sample_videos[0].caption

    def test_save_without_filepath_raises_error(self, sample_videos):
        """Test that save without filepath raises error."""
        viio = VIIO()

        with pytest.raises(VIIOError, match="No filepath provided"):
            viio.save(sample_videos)

    def test_load_without_filepath_raises_error(self):
        """Test that load without filepath raises error."""
        viio = VIIO()

        with pytest.raises(VIIOError, match="No filepath provided"):
            viio.load()

    def test_load_nonexistent_file_raises_error(self):
        """Test loading a non-existent file raises error."""
        viio = VIIO(Path("nonexistent.viio"))

        with pytest.raises(FileNotFoundError):
            viio.load()

    def test_load_invalid_magic_raises_error(self, temp_file):
        """Test loading file with invalid magic header raises error."""
        temp_file.write_bytes(b"FAKE" + bytes([1]) + b"some data")

        viio = VIIO(temp_file)
        with pytest.raises(InvalidFileError, match="Invalid file header"):
            viio.load()

    def test_load_file_too_small_raises_error(self, temp_file):
        """Test loading file that's too small raises error."""
        temp_file.write_bytes(b"VI")

        viio = VIIO(temp_file)
        with pytest.raises(InvalidFileError, match="File too small"):
            viio.load()

    def test_load_unsupported_version_raises_error(self, temp_file):
        """Test loading file with unsupported version raises error."""
        temp_file.write_bytes(VIIO.MAGIC + bytes([255]) + b"data")

        viio = VIIO(temp_file)
        with pytest.raises(InvalidFileError, match="Unsupported file version"):
            viio.load()

    def test_load_corrupted_data_raises_error(self, temp_file):
        """Test loading corrupted data raises error."""
        temp_file.write_bytes(VIIO.MAGIC + bytes([1]) + b"corrupted data")

        viio = VIIO(temp_file)
        with pytest.raises(InvalidFileError, match="Corrupted file data"):
            viio.load()

    def test_save_creates_directory(self, sample_videos):
        """Test that save creates parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "subdir" / "test.viio"
            viio = VIIO(filepath)

            viio.save(sample_videos)
            assert filepath.exists()
            assert filepath.parent.exists()

    def test_save_adds_extension(self, sample_videos):
        """Test that save adds .viio extension if missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test"
            viio = VIIO(filepath)

            saved_path = viio.save(sample_videos)
            assert saved_path.suffix == ".viio"

    def test_quick_save(self, sample_videos, temp_file):
        """Test quick_save class method."""
        saved_path = VIIO.quick_save(sample_videos, temp_file)
        assert saved_path.exists()

    def test_quick_load(self, sample_videos, temp_file):
        """Test quick_load class method."""
        VIIO.quick_save(sample_videos, temp_file)
        loaded_videos = VIIO.quick_load(temp_file)

        assert len(loaded_videos) == len(sample_videos)
        assert loaded_videos[0].caption == sample_videos[0].caption

    def test_roundtrip_preserves_data(self, sample_videos, temp_file):
        """Test that save/load roundtrip preserves all data."""
        viio = VIIO(temp_file)
        viio.save(sample_videos)
        loaded = viio.load()

        for original, restored in zip(sample_videos, loaded):
            assert original.no == restored.no
            assert original.caption == restored.caption
            assert original.username == restored.username
            assert original.video_id == restored.video_id
            assert original._type == restored._type
            assert original.url == restored.url
            assert original.duration == restored.duration
            assert original.status == restored.status
            assert original.percentage == restored.percentage

    def test_save_empty_list(self, temp_file):
        """Test saving an empty list of videos."""
        viio = VIIO(temp_file)
        viio.save([])
        loaded = viio.load()

        assert loaded == []

    def test_save_with_unicode_characters(self, temp_file):
        """Test saving videos with unicode characters in captions."""
        videos = [
            Video(
                caption="Test \u65e5\u672c\u8a9e \u0627\u0644\u0639\u0631\u0628\u064a\u0629 \u4e2d\u6587",
                username="user",
                video_id="test123",
                _type=VideoType.VIDEO,
            )
        ]

        viio = VIIO(temp_file)
        viio.save(videos)
        loaded = viio.load()

        assert loaded[0].caption == "Test \u65e5\u672c\u8a9e \u0627\u0644\u0639\u0631\u0628\u064a\u0629 \u4e2d\u6587"
