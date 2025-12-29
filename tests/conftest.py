"""
Pytest configuration and shared fixtures for ViDownloader tests.
"""
import pytest
import sys
import os

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
