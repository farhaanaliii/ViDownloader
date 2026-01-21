"""
Unit tests for vidownloader.core.Models module.
Tests dataclasses, serialization, and deserialization.
"""
import pytest

from vidownloader.core.Models import Link, Video, Bridge, DownloaderEvent, ScraperEvent
from vidownloader.core.Constants import VideoType, BridgeType, EventType


class TestLink:
    """Tests for the Link dataclass."""

    def test_link_creation(self):
        """Test creating a Link with required fields."""
        link = Link(
            url="https://www.youtube.com/watch?v=test123",
            video_type=VideoType.VIDEO,
            username="testuser",
            video_id="test123"
        )
        
        assert link.url == "https://www.youtube.com/watch?v=test123"
        assert link.video_type == VideoType.VIDEO
        assert link.username == "testuser"
        assert link.video_id == "test123"

    def test_link_with_playlist(self):
        """Test creating a Link with playlist information."""
        link = Link(
            url="https://www.youtube.com/watch?v=test123&list=PLtest",
            video_type=VideoType.VIDEO,
            username="testuser",
            video_id="test123",
            playlist_id="PLtest",
            playlist_name="Test Playlist"
        )
        
        assert link.playlist_id == "PLtest"
        assert link.playlist_name == "Test Playlist"

    def test_link_short_type(self):
        """Test creating a Link for a Short."""
        link = Link(
            url="https://www.youtube.com/shorts/abc123",
            video_type=VideoType.SHORT
        )
        
        assert link.video_type == VideoType.SHORT


class TestVideo:
    """Tests for the Video dataclass."""

    def test_video_creation(self):
        """Test creating a Video with required fields."""
        video = Video(
            caption="Test Video",
            username="testuser",
            video_id="test123",
            _type=VideoType.VIDEO
        )
        
        assert video.caption == "Test Video"
        assert video.username == "testuser"
        assert video.video_id == "test123"
        assert video._type == VideoType.VIDEO
        assert video.status == "Pending"
        assert video.percentage == "0%"

    def test_video_with_all_fields(self):
        """Test creating a Video with all fields."""
        video = Video(
            no=1,
            caption="Test Video",
            percentage="50%",
            status="Downloading",
            username="testuser",
            video_id="test123",
            _type=VideoType.VIDEO,
            url="https://www.youtube.com/watch?v=test123",
            duration=180,
            playlist_id="PLtest",
            playlist_name="Test Playlist"
        )
        
        assert video.no == 1
        assert video.percentage == "50%"
        assert video.status == "Downloading"
        assert video.duration == 180
        assert video.playlist_id == "PLtest"

    def test_video_to_dict(self):
        """Test Video serialization to dictionary."""
        video = Video(
            caption="Test Video",
            username="testuser",
            video_id="test123",
            _type=VideoType.VIDEO,
            duration=120
        )
        
        video_dict = video.to_dict()
        
        assert isinstance(video_dict, dict)
        assert video_dict["caption"] == "Test Video"
        assert video_dict["username"] == "testuser"
        assert video_dict["video_id"] == "test123"
        assert video_dict["_type"] == VideoType.VIDEO.value
        assert video_dict["duration"] == 120

    def test_video_from_dict(self):
        """Test Video deserialization from dictionary."""
        video_dict = {
            "no": 1,
            "caption": "Test Video",
            "percentage": "75%",
            "status": "Complete",
            "username": "testuser",
            "video_id": "test123",
            "_type": VideoType.SHORT.value,
            "url": "https://www.youtube.com/shorts/test123",
            "duration": 60,
            "playlist_id": None,
            "playlist_name": None
        }
        
        video = Video.from_dict(video_dict)
        
        assert video.no == 1
        assert video.caption == "Test Video"
        assert video.percentage == "75%"
        assert video.status == "Complete"
        assert video._type == VideoType.SHORT
        assert video.duration == 60

    def test_video_roundtrip(self):
        """Test Video serialization and deserialization roundtrip."""
        original = Video(
            no=5,
            caption="Roundtrip Test",
            username="testuser",
            video_id="roundtrip123",
            _type=VideoType.VIDEO,
            duration=300
        )
        
        video_dict = original.to_dict()
        restored = Video.from_dict(video_dict)
        
        assert restored.no == original.no
        assert restored.caption == original.caption
        assert restored.username == original.username
        assert restored.video_id == original.video_id
        assert restored._type == original._type
        assert restored.duration == original.duration

    def test_video_str_representation(self):
        """Test Video __str__ method."""
        video = Video(
            caption="Test",
            username="user",
            video_id="123",
            _type=VideoType.VIDEO
        )
        
        str_repr = str(video)
        assert "Test" in str_repr
        assert "user" in str_repr
        assert "123" in str_repr

    def test_video_repr(self):
        """Test Video __repr__ method."""
        video = Video(
            no=1,
            caption="Test",
            username="user",
            video_id="123",
            _type=VideoType.VIDEO
        )
        
        repr_str = repr(video)
        assert "Video" in repr_str
        assert "Test" in repr_str


class TestBridge:
    """Tests for the Bridge dataclass."""

    def test_bridge_with_links(self):
        """Test creating a Bridge with links."""
        links = [
            Link(url="http://example.com/1", video_type=VideoType.VIDEO),
            Link(url="http://example.com/2", video_type=VideoType.SHORT)
        ]
        
        bridge = Bridge(bridge_type=BridgeType.LINKS, links=links)
        
        assert bridge.bridge_type == BridgeType.LINKS
        assert len(bridge.links) == 2

    def test_bridge_with_videos(self):
        """Test creating a Bridge with videos."""
        videos = [
            Video(caption="Video 1", username="user", video_id="1", _type=VideoType.VIDEO)
        ]
        
        bridge = Bridge(bridge_type=BridgeType.IMPORTED, videos=videos)
        
        assert bridge.bridge_type == BridgeType.IMPORTED
        assert len(bridge.videos) == 1


class TestDownloaderEvent:
    """Tests for the DownloaderEvent dataclass."""

    def test_downloader_event_creation(self):
        """Test creating a DownloaderEvent."""
        from pathlib import Path
        
        event = DownloaderEvent(
            event=EventType.PROGRESS,
            video_id=1,
            progress="50%",
            status="Downloading"
        )
        
        assert event.event == EventType.PROGRESS
        assert event.video_id == 1
        assert event.progress == "50%"
        assert event.status == "Downloading"


class TestScraperEvent:
    """Tests for the ScraperEvent dataclass."""

    def test_scraper_event_creation(self):
        """Test creating a ScraperEvent."""
        videos = [
            Video(caption="Test", username="user", video_id="123", _type=VideoType.VIDEO)
        ]
        
        event = ScraperEvent(
            event=EventType.VIDEOS,
            videos=videos,
            message="Scraping complete"
        )
        
        assert event.event == EventType.VIDEOS
        assert len(event.videos) == 1
        assert event.message == "Scraping complete"
