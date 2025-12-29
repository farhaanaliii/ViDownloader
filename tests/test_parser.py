"""
Unit tests for vidownloader.core.Worker.Parser module.
Tests YouTube response parsing functionality.
"""
import pytest

from vidownloader.core.Worker.Parser import Parser
from vidownloader.core.Constants import VideoType


class TestParser:
    """Tests for the Parser class."""

    def test_parse_videos_from_channel_data(self, sample_video_data):
        """Test parsing video data from a channel response."""
        videos, token = Parser.parse_channel_videos_or_shorts_and_token(
            sample_video_data,
            VideoType.VIDEO,
            "testuser"
        )
        
        assert len(videos) == 1
        assert videos[0].video_id == "test123"
        assert videos[0].caption == "Test Video Title"
        assert videos[0].username == "testuser"
        assert videos[0]._type == VideoType.VIDEO

    def test_parse_shorts_from_channel_data(self, sample_shorts_data):
        """Test parsing shorts data from a channel response."""
        videos, token = Parser.parse_channel_videos_or_shorts_and_token(
            sample_shorts_data,
            VideoType.SHORT,
            "testuser"
        )
        
        assert len(videos) == 1
        assert videos[0].video_id == "short123"
        assert videos[0].caption == "Test Short Title"
        assert videos[0]._type == VideoType.SHORT

    def test_parse_empty_data(self):
        """Test parsing empty data returns empty list."""
        videos, token = Parser.parse_channel_videos_or_shorts_and_token(
            {},
            VideoType.VIDEO,
            "testuser"
        )
        
        assert videos == []
        assert token is None

    def test_parse_malformed_data(self):
        """Test parsing malformed data doesn't crash."""
        malformed_data = {
            "contents": {
                "unexpected": "structure"
            }
        }
        
        videos, token = Parser.parse_channel_videos_or_shorts_and_token(
            malformed_data,
            VideoType.VIDEO,
            "testuser"
        )
        
        # Should return empty list, not crash
        assert videos == []

    def test_video_url_format(self, sample_video_data):
        """Test that video URLs are correctly formatted."""
        videos, _ = Parser.parse_channel_videos_or_shorts_and_token(
            sample_video_data,
            VideoType.VIDEO,
            "testuser"
        )
        
        assert len(videos) == 1
        assert videos[0].url == "https://www.youtube.com/watch?v=test123"

    def test_shorts_url_format(self, sample_shorts_data):
        """Test that shorts URLs are correctly formatted."""
        videos, _ = Parser.parse_channel_videos_or_shorts_and_token(
            sample_shorts_data,
            VideoType.SHORT,
            "testuser"
        )
        
        assert len(videos) == 1
        assert videos[0].url == "https://www.youtube.com/shorts/short123"

    def test_continuation_token_extraction(self):
        """Test extraction of continuation token for pagination."""
        data_with_token = {
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
                                                            "videoId": "abc123",
                                                            "title": {"runs": [{"text": "Video"}]}
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "continuationItemRenderer": {
                                                    "continuationEndpoint": {
                                                        "continuationCommand": {
                                                            "token": "next_page_token_123"
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
        
        videos, token = Parser.parse_channel_videos_or_shorts_and_token(
            data_with_token,
            VideoType.VIDEO,
            "testuser"
        )
        
        assert token == "next_page_token_123"
