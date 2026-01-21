"""
Pytest configuration and shared fixtures for ViDownloader tests.
"""
import pytest
import sys
import os
import tempfile
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(scope="session")
def qapp():
    """
    Create a QApplication instance for the entire test session.
    Required for any PyQt5 widget tests.
    """
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_video_data():
    """Sample video data for testing parser."""
    return {
        "contents": {
            "twoColumnBrowseResultsRenderer": {
                "tabs": [
                    {
                        "tabRenderer": {
                            "title": "Videos",
                            "content": {
                                "richGridRenderer": {
                                    "contents": [
                                        {
                                            "richItemRenderer": {
                                                "content": {
                                                    "videoRenderer": {
                                                        "videoId": "test123",
                                                        "title": {
                                                            "runs": [{"text": "Test Video Title"}]
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    ]
                                }
                            }
                        }
                    }
                ]
            }
        }
    }


@pytest.fixture
def sample_shorts_data():
    """Sample shorts data for testing parser."""
    return {
        "contents": {
            "twoColumnBrowseResultsRenderer": {
                "tabs": [
                    {
                        "tabRenderer": {
                            "title": "Shorts",
                            "content": {
                                "richGridRenderer": {
                                    "contents": [
                                        {
                                            "richItemRenderer": {
                                                "content": {
                                                    "shortsLockupViewModel": {
                                                        "entityId": "shorts-shelf-item-short123",
                                                        "overlayMetadata": {
                                                            "primaryText": {
                                                                "content": "Test Short Title"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    ]
                                }
                            }
                        }
                    }
                ]
            }
        }
    }


@pytest.fixture
def sample_link():
    """Sample Link object for testing."""
    from vidownloader.core.Models import Link
    from vidownloader.core.Constants import VideoType
    
    return Link(
        url="https://www.youtube.com/watch?v=test123",
        video_type=VideoType.VIDEO,
        username="testuser",
        video_id="test123"
    )


@pytest.fixture
def sample_video():
    """Sample Video object for testing."""
    from vidownloader.core.Models import Video
    from vidownloader.core.Constants import VideoType
    
    return Video(
        no=1,
        caption="Test Video",
        username="testuser",
        video_id="test123",
        _type=VideoType.VIDEO,
        url="https://www.youtube.com/watch?v=test123",
        duration=120
    )


@pytest.fixture
def sample_videos_list():
    """Sample list of Video objects for testing."""
    from vidownloader.core.Models import Video
    from vidownloader.core.Constants import VideoType
    
    return [
        Video(
            no=1,
            caption="Test Video 1",
            username="testuser",
            video_id="video1",
            _type=VideoType.VIDEO,
            duration=120
        ),
        Video(
            no=2,
            caption="Test Short 1",
            username="testuser",
            video_id="short1",
            _type=VideoType.SHORT,
            duration=30
        ),
    ]

