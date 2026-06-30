"""
Unit tests for vidownloader.core.Worker.Parser module.
Tests YouTube response parsing functionality.
"""

import pytest

from vidownloader.core.Constants import VideoType
from vidownloader.core.Worker.Parser import Parser


class TestParser:
    """Tests for the Parser class."""

    def test_parse_videos_from_channel_data(self, sample_video_data):
        """Test parsing video data from a channel response."""
        videos, token = Parser.parse_channel_videos_or_shorts_and_token(
            sample_video_data, VideoType.VIDEO, "testuser"
        )

        assert len(videos) == 1
        assert videos[0].video_id == "test123"
        assert videos[0].caption == "Test Video Title"
        assert videos[0].username == "testuser"
        assert videos[0]._type == VideoType.VIDEO

    def test_parse_shorts_from_channel_data(self, sample_shorts_data):
        """Test parsing shorts data from a channel response."""
        videos, token = Parser.parse_channel_videos_or_shorts_and_token(
            sample_shorts_data, VideoType.SHORT, "testuser"
        )

        assert len(videos) == 1
        assert videos[0].video_id == "short123"
        assert videos[0].caption == "Test Short Title"
        assert videos[0]._type == VideoType.SHORT

    def test_parse_empty_data(self):
        """Test parsing empty data returns empty list."""
        videos, token = Parser.parse_channel_videos_or_shorts_and_token(
            {}, VideoType.VIDEO, "testuser"
        )

        assert videos == []
        assert token is None

    def test_parse_malformed_data(self):
        """Test parsing malformed data doesn't crash."""
        malformed_data = {"contents": {"unexpected": "structure"}}

        videos, token = Parser.parse_channel_videos_or_shorts_and_token(
            malformed_data, VideoType.VIDEO, "testuser"
        )

        # Should return empty list, not crash
        assert videos == []

    def test_video_url_format(self, sample_video_data):
        """Test that video URLs are correctly formatted."""
        videos, _ = Parser.parse_channel_videos_or_shorts_and_token(
            sample_video_data, VideoType.VIDEO, "testuser"
        )

        assert len(videos) == 1
        assert videos[0].url == "https://www.youtube.com/watch?v=test123"

    def test_shorts_url_format(self, sample_shorts_data):
        """Test that shorts URLs are correctly formatted."""
        videos, _ = Parser.parse_channel_videos_or_shorts_and_token(
            sample_shorts_data, VideoType.SHORT, "testuser"
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
                                                        "lockupViewModel": {
                                                            "contentId": "abc123",
                                                            "metadata": {
                                                                "lockupMetadataViewModel": {
                                                                    "title": {
                                                                        "content": "Video"
                                                                    }
                                                                }
                                                            },
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
                                            },
                                        ]
                                    }
                                },
                            }
                        }
                    ]
                }
            }
        }

        videos, token = Parser.parse_channel_videos_or_shorts_and_token(
            data_with_token, VideoType.VIDEO, "testuser"
        )

        assert token == "next_page_token_123"

    def test_parse_with_duration(self):
        """Test parsing videos with duration information."""
        data_with_duration = {
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
                                                        "lockupViewModel": {
                                                            "contentId": "test123",
                                                            "metadata": {
                                                                "lockupMetadataViewModel": {
                                                                    "title": {
                                                                        "content": "Test Video"
                                                                    }
                                                                }
                                                            },
                                                            "lengthText": {
                                                                "simpleText": "3:45"
                                                            },
                                                        }
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                },
                            }
                        }
                    ]
                }
            }
        }

        videos, _ = Parser.parse_channel_videos_or_shorts_and_token(
            data_with_duration, VideoType.VIDEO, "testuser"
        )

        assert len(videos) == 1
        assert videos[0].duration == "3:45"

    def test_multiple_videos_parsing(self):
        """Test parsing multiple videos from channel."""
        data_multiple = {
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
                                                        "lockupViewModel": {
                                                            "contentId": "video1",
                                                            "metadata": {
                                                                "lockupMetadataViewModel": {
                                                                    "title": {
                                                                        "content": "Video 1"
                                                                    }
                                                                }
                                                            },
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "richItemRenderer": {
                                                    "content": {
                                                        "lockupViewModel": {
                                                            "contentId": "video2",
                                                            "metadata": {
                                                                "lockupMetadataViewModel": {
                                                                    "title": {
                                                                        "content": "Video 2"
                                                                    }
                                                                }
                                                            },
                                                        }
                                                    }
                                                }
                                            },
                                        ]
                                    }
                                },
                            }
                        }
                    ]
                }
            }
        }

        videos, _ = Parser.parse_channel_videos_or_shorts_and_token(
            data_multiple, VideoType.VIDEO, "testuser"
        )

        assert len(videos) == 2
        assert videos[0].video_id == "video1"
        assert videos[1].video_id == "video2"


class TestParserPlaylist:
    """Tests for Parser playlist-related methods."""

    def test_extract_playlist_name(self):
        """Test extracting playlist name from API response."""
        data = {"header": {"pageHeaderRenderer": {"pageTitle": "My Awesome Playlist"}}}

        name = Parser.extract_playlist_name(data)
        assert name == "My Awesome Playlist"

    def test_extract_playlist_name_missing(self):
        """Test extracting playlist name when not present."""
        data = {"header": {}}

        name = Parser.extract_playlist_name(data)
        assert name is None

    def test_extract_playlist_name_empty_data(self):
        """Test extracting playlist name from empty data."""
        name = Parser.extract_playlist_name({})
        assert name is None

    def test_parse_playlist_videos(self):
        """Test parsing videos from playlist response."""
        data = {
            "contents": {
                "twoColumnBrowseResultsRenderer": {
                    "tabs": [
                        {
                            "tabRenderer": {
                                "content": {
                                    "sectionListRenderer": {
                                        "contents": [
                                            {
                                                "itemSectionRenderer": {
                                                    "contents": [
                                                        {
                                                            "lockupViewModel": {
                                                                "contentId": "playlist_vid1",
                                                                "metadata": {
                                                                    "lockupMetadataViewModel": {
                                                                        "title": {
                                                                            "content": "Playlist Video 1"
                                                                        },
                                                                        "metadata": {
                                                                            "contentMetadataViewModel": {
                                                                                "metadataRows": [
                                                                                    {
                                                                                        "metadataParts": [
                                                                                            {
                                                                                                "text": {
                                                                                                    "content": "Creator1"
                                                                                                }
                                                                                            }
                                                                                        ]
                                                                                    }
                                                                                ]
                                                                            }
                                                                        },
                                                                    }
                                                                },
                                                                "contentImage": {
                                                                    "thumbnailViewModel": {
                                                                        "overlays": [
                                                                            {
                                                                                "thumbnailBottomOverlayViewModel": {
                                                                                    "badges": [
                                                                                        {
                                                                                            "thumbnailBadgeViewModel": {
                                                                                                "text": "3:00"
                                                                                            }
                                                                                        }
                                                                                    ]
                                                                                }
                                                                            }
                                                                        ]
                                                                    }
                                                                },
                                                            }
                                                        }
                                                    ]
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

        videos, token = Parser.parse_playlist_videos_and_token(data)

        assert len(videos) == 1
        assert videos[0].video_id == "playlist_vid1"
        assert videos[0].caption == "Playlist Video 1"
        assert videos[0].username == "Creator1"
        assert videos[0].duration == "3:00"

    def test_parse_playlist_videos_with_continuation(self):
        """Test parsing playlist videos with continuation token."""
        data = {
            "contents": {
                "twoColumnBrowseResultsRenderer": {
                    "tabs": [
                        {
                            "tabRenderer": {
                                "content": {
                                    "sectionListRenderer": {
                                        "contents": [
                                            {
                                                "itemSectionRenderer": {
                                                    "contents": [
                                                        {
                                                            "lockupViewModel": {
                                                                "contentId": "vid1",
                                                                "metadata": {
                                                                    "lockupMetadataViewModel": {
                                                                        "title": {
                                                                            "content": "Video 1"
                                                                        },
                                                                        "metadata": {
                                                                            "contentMetadataViewModel": {
                                                                                "metadataRows": [
                                                                                    {
                                                                                        "metadataParts": [
                                                                                            {
                                                                                                "text": {
                                                                                                    "content": "Creator"
                                                                                                }
                                                                                            }
                                                                                        ]
                                                                                    }
                                                                                ]
                                                                            }
                                                                        },
                                                                    }
                                                                },
                                                                "contentImage": {
                                                                    "thumbnailViewModel": {
                                                                        "overlays": [
                                                                            {
                                                                                "thumbnailBottomOverlayViewModel": {
                                                                                    "badges": [
                                                                                        {
                                                                                            "thumbnailBadgeViewModel": {
                                                                                                "text": "3:00"
                                                                                            }
                                                                                        }
                                                                                    ]
                                                                                }
                                                                            }
                                                                        ]
                                                                    }
                                                                },
                                                            }
                                                        },
                                                        {
                                                            "continuationItemRenderer": {
                                                                "continuationEndpoint": {
                                                                    "continuationCommand": {
                                                                        "token": "playlist_token_123"
                                                                    }
                                                                }
                                                            }
                                                        },
                                                    ]
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

        videos, token = Parser.parse_playlist_videos_and_token(data)

        assert len(videos) == 1
        assert token == "playlist_token_123"

    def test_parse_playlist_continuation_response(self):
        """Test parsing playlist continuation response."""
        data = {
            "onResponseReceivedActions": [
                {
                    "appendContinuationItemsAction": {
                        "continuationItems": [
                            {
                                "lockupViewModel": {
                                    "contentId": "cont_vid1",
                                    "metadata": {
                                        "lockupMetadataViewModel": {
                                            "title": {"content": "Continuation Video"},
                                            "metadata": {
                                                "contentMetadataViewModel": {
                                                    "metadataRows": [
                                                        {
                                                            "metadataParts": [
                                                                {
                                                                    "text": {
                                                                        "content": "Creator2"
                                                                    }
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            },
                                        }
                                    },
                                    "contentImage": {
                                        "thumbnailViewModel": {
                                            "overlays": [
                                                {
                                                    "thumbnailBottomOverlayViewModel": {
                                                        "badges": [
                                                            {
                                                                "thumbnailBadgeViewModel": {
                                                                    "text": "3:00"
                                                                }
                                                            }
                                                        ]
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                }
                            }
                        ]
                    }
                }
            ]
        }

        videos, _ = Parser.parse_playlist_videos_and_token(data)

        assert len(videos) == 1
        assert videos[0].video_id == "cont_vid1"
        assert videos[0].caption == "Continuation Video"

    def test_parse_playlist_empty_data(self):
        """Test parsing empty playlist data."""
        videos, token = Parser.parse_playlist_videos_and_token({})

        assert videos == []
        assert token is None


class TestParserVideoDetails:
    """Tests for Parser.parse_video_details method."""

    def test_parse_video_details(self):
        """Test parsing individual video details."""
        data = {
            "videoDetails": {
                "videoId": "detail_vid1",
                "title": "Detailed Video Title",
                "lengthSeconds": "300",
            },
            "microformat": {
                "playerMicroformatRenderer": {
                    "ownerProfileUrl": "https://www.youtube.com/@testcreator"
                }
            },
        }

        video = Parser.parse_video_details(data)

        assert video is not None
        assert video.video_id == "detail_vid1"
        assert video.caption == "Detailed Video Title"
        assert video.username == "testcreator"
        assert video.duration == "300"
        assert video.url == "https://www.youtube.com/watch?v=detail_vid1"

    def test_parse_video_details_no_username(self):
        """Test parsing video details without username."""
        data = {"videoDetails": {"videoId": "vid123", "title": "Test Video"}}

        video = Parser.parse_video_details(data)

        assert video is not None
        assert video.video_id == "vid123"
        assert video.username == ""

    def test_parse_video_details_invalid_duration(self):
        """Test parsing video details with invalid duration."""
        data = {
            "videoDetails": {
                "videoId": "vid123",
                "title": "Test",
                "lengthSeconds": "invalid",
            }
        }

        video = Parser.parse_video_details(data)

        assert video is not None
        assert video.duration == "invalid"

    def test_parse_video_details_empty_data(self):
        """Test parsing empty video details."""
        video = Parser.parse_video_details({})
        assert video is None

    def test_parse_video_details_missing_video_details(self):
        """Test parsing when videoDetails key is missing."""
        data = {"microformat": {}}

        video = Parser.parse_video_details(data)
        assert video is None


class TestParserContinuationToken:
    """Tests for Parser._extract_continuation_token method."""

    def test_extract_simple_continuation_token(self):
        """Test extracting simple continuation token."""
        item = {
            "continuationItemRenderer": {
                "continuationEndpoint": {
                    "continuationCommand": {"token": "simple_token_123"}
                }
            }
        }

        token = Parser._extract_continuation_token(item)
        assert token == "simple_token_123"

    def test_extract_nested_continuation_token(self):
        """Test extracting nested continuation token."""
        item = {
            "continuationItemRenderer": {
                "continuationEndpoint": {
                    "commandExecutorCommand": {
                        "commands": [
                            {"continuationCommand": {"token": "nested_token_456"}}
                        ]
                    }
                }
            }
        }

        token = Parser._extract_continuation_token(item)
        assert token == "nested_token_456"

    def test_extract_no_continuation_token(self):
        """Test extracting when no token present."""
        item = {"continuationItemRenderer": {}}

        token = Parser._extract_continuation_token(item)
        assert token is None

    def test_extract_empty_item(self):
        """Test extracting from empty item."""
        token = Parser._extract_continuation_token({})
        assert token is None
