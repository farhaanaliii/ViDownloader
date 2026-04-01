import traceback

from vidownloader.core import Logger
from vidownloader.core.Constants import VideoType
from vidownloader.core.Models import Video

logger = Logger.get_logger("Parser")


class Parser:

    @staticmethod  # what a long name :(
    def parse_channel_videos_or_shorts_and_token(
        data: dict, video_type: VideoType, username: str
    ) -> tuple[list[Video], str]:
        videos = []
        continuation_token = None
        is_videos = video_type == VideoType.VIDEO

        _RENDERER_ = "videoRenderer" if is_videos else "shortsLockupViewModel"
        _ID_ = "videoId" if is_videos else "entityId"
        _TITLE = "title" if is_videos else "overlayMetadata"

        try:
            raw_content_list = None
            if data.get("onResponseReceivedActions"):
                raw_content_list = data["onResponseReceivedActions"][0][
                    "appendContinuationItemsAction"
                ]["continuationItems"]
            else:
                tabs = data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"]
                target_tab = None

                for tab in tabs:
                    tab = tab["tabRenderer"]
                    if tab["title"] == video_type.capitalize():
                        target_tab = tab
                        break

                if not target_tab:
                    return None, None

                raw_content_list = target_tab["content"]["richGridRenderer"]["contents"]

            if not raw_content_list:
                return None, None

            # continuation token is usually in the last item
            continuation_token = (
                raw_content_list[-1]
                .get("continuationItemRenderer", {})
                .get("continuationEndpoint", {})
                .get("continuationCommand", {})
                .get("token")
            )
            for content in raw_content_list:
                renderer = (
                    content.get("richItemRenderer", {})
                    .get("content", {})
                    .get(_RENDERER_)
                )
                if not renderer:
                    continue

                title_ = renderer[_TITLE]

                if is_videos:
                    title = title_["runs"][0]["text"]
                else:
                    title = title_["primaryText"]["content"]

                video_id = renderer[_ID_]
                if not is_videos:
                    video_id = video_id.replace("shorts-shelf-item-", "")

                # Extract duration if available
                duration = None
                if is_videos:
                    length_text = renderer.get("lengthText", {}).get("simpleText", "")
                    # Parse duration from format like "3:45" or "1:23:45"
                    if length_text:
                        try:
                            parts = length_text.split(":")
                            if len(parts) == 2:  # MM:SS
                                duration = int(parts[0]) * 60 + int(parts[1])
                            elif len(parts) == 3:  # HH:MM:SS
                                duration = (
                                    int(parts[0]) * 3600
                                    + int(parts[1]) * 60
                                    + int(parts[2])
                                )
                        except (ValueError, IndexError):
                            pass

                videos.append(
                    Video(
                        caption=title,
                        username=username,
                        video_id=video_id,
                        _type=video_type,
                        url=(
                            f"https://www.youtube.com/watch?v={video_id}"
                            if is_videos
                            else f"https://www.youtube.com/shorts/{video_id}"
                        ),
                        duration=duration,
                    )
                )

            return videos, continuation_token
        except Exception as e:
            logger.error("Error parsing videos: %s", str(e))
            logger.error(traceback.format_exc())
            return videos, continuation_token

    @staticmethod
    def _extract_continuation_token(continuation_item: dict) -> str | None:
        continuation_renderer = continuation_item.get("continuationItemRenderer", {})
        continuation_endpoint = continuation_renderer.get("continuationEndpoint", {})

        # Try simple path first: continuationEndpoint -> continuationCommand -> token
        simple_token = continuation_endpoint.get("continuationCommand", {}).get("token")
        if simple_token:
            return simple_token

        # Try nested path: continuationEndpoint -> commandExecutorCommand -> commands[] -> continuationCommand -> token
        command_executor = continuation_endpoint.get("commandExecutorCommand", {})
        commands = command_executor.get("commands", [])
        for cmd in commands:
            token = cmd.get("continuationCommand", {}).get("token")
            if token:
                return token

        return None

    @staticmethod
    def extract_playlist_name(data: dict) -> str | None:
        """Extract playlist name from initial playlist API response"""
        try:
            # Primary path: header -> pageHeaderRenderer -> pageTitle
            header = data.get("header", {})
            playlist_header = header.get("pageHeaderRenderer", {})
            title = playlist_header.get("pageTitle", None)

            # Fallback path: metadata -> playlistMetadataRenderer -> title
            if not title:
                metadata = data.get("metadata", {})
                playlist_metadata = metadata.get("playlistMetadataRenderer", {})
                title = playlist_metadata.get("title", None)

            return title
        except Exception as e:
            logger.debug(f"Error extracting playlist name: {e}")
            return None

    @staticmethod
    def parse_playlist_videos_and_token(data: dict) -> tuple[list[Video], str]:
        videos = []
        continuation_token = None

        try:
            raw_content_list = None

            # Extract playlist owner as fallback for videos without uploader info
            playlist_owner = None
            try:
                microformat = data.get("microformat", {})
                microformat_data = microformat.get("microformatDataRenderer", {})
                course_details = microformat_data.get("courseDetails", {})
                playlist_owner = course_details.get("providerName", None)
            except Exception:
                pass

            if data.get("onResponseReceivedActions"):
                actions = data["onResponseReceivedActions"]
                for action in actions:
                    if "appendContinuationItemsAction" in action:
                        raw_content_list = action["appendContinuationItemsAction"][
                            "continuationItems"
                        ]
                        break

                # For continuation responses, token is in the content list
                if raw_content_list:
                    for content in reversed(raw_content_list):
                        if "continuationItemRenderer" in content:
                            continuation_token = Parser._extract_continuation_token(
                                content
                            )
                            if continuation_token:
                                break
            else:
                # Initial playlist response
                # Path: contents -> twoColumnBrowseResultsRenderer -> tabs -> tabRenderer -> content
                #       -> sectionListRenderer -> contents -> itemSectionRenderer -> playlistVideoListRenderer
                # The continuation token is INSIDE playlistVideoListRenderer.contents as the LAST item
                tabs = (
                    data.get("contents", {})
                    .get("twoColumnBrowseResultsRenderer", {})
                    .get("tabs", [])
                )

                for tab in tabs:
                    tab_content = tab.get("tabRenderer", {}).get("content", {})
                    section_list_contents = tab_content.get(
                        "sectionListRenderer", {}
                    ).get("contents", [])

                    for section in section_list_contents:
                        item_section = section.get("itemSectionRenderer", {}).get(
                            "contents", []
                        )
                        for item in item_section:
                            playlist_renderer = item.get(
                                "playlistVideoListRenderer", {}
                            )
                            if playlist_renderer:
                                raw_content_list = playlist_renderer.get("contents", [])

                                # Token is INSIDE the playlist contents as the LAST item
                                if raw_content_list:
                                    last_item = raw_content_list[-1]
                                    if "continuationItemRenderer" in last_item:
                                        continuation_token = (
                                            Parser._extract_continuation_token(
                                                last_item
                                            )
                                        )
                                break

                    if raw_content_list:
                        break

            if not raw_content_list:
                logger.debug("No raw_content_list found in playlist response")
                return videos, continuation_token

            logger.debug(
                f"Found {len(raw_content_list)} items in raw_content_list, continuation_token: {continuation_token[:50] if continuation_token else None}..."
            )

            for content in raw_content_list:
                renderer = content.get("playlistVideoRenderer")
                if not renderer:
                    continue

                video_id = renderer.get("videoId")
                if not video_id:
                    continue

                title = ""
                title_obj = renderer.get("title", {})
                if "runs" in title_obj:
                    title = title_obj["runs"][0].get("text", "")
                elif "simpleText" in title_obj:
                    title = title_obj.get("simpleText", "")

                uploader = ""
                byline = renderer.get("shortBylineText", {})
                if "runs" in byline:
                    uploader = byline["runs"][0].get("text", "")

                # Fallback: If uploader not found, use playlist owner (videos uploaded by playlist owner)
                if not uploader and playlist_owner:
                    uploader = playlist_owner

                # Extract duration (in seconds)
                duration = None
                length_text = renderer.get("lengthSeconds")
                if length_text:
                    try:
                        duration = int(length_text)
                    except (ValueError, TypeError):
                        pass

                videos.append(
                    Video(
                        caption=title,
                        username=uploader,
                        video_id=video_id,
                        _type=VideoType.VIDEO,
                        url=f"https://www.youtube.com/watch?v={video_id}",
                        duration=duration,
                    )
                )

            return videos, continuation_token

        except Exception as e:
            logger.error("Error parsing playlist: %s", str(e))
            logger.error(traceback.format_exc())
            return videos, continuation_token

    @staticmethod
    def parse_video_details(data: dict) -> Video | None:
        try:
            video_renderer = data.get("videoDetails", {})
            if not video_renderer:
                return None

            video_id = video_renderer.get("videoId", "")
            title = video_renderer.get("title", "")

            # Extract duration in seconds
            duration = None
            duration_str = video_renderer.get("lengthSeconds")
            if duration_str:
                try:
                    duration = int(duration_str)
                except (ValueError, TypeError):
                    duration = None

            # Extract username from ownerProfileUrl
            owner_url = (
                data.get("microformat", {})
                .get("playerMicroformatRenderer", {})
                .get("ownerProfileUrl", "")
            )
            username = ""
            if "/@" in owner_url:
                username = owner_url.split("/@")[-1].rstrip("/")

            return Video(
                caption=title,
                username=username,
                video_id=video_id,
                _type=VideoType.VIDEO,
                url=f"https://www.youtube.com/watch?v={video_id}",
                duration=duration,
            )
        except Exception as e:
            logger.error("Error parsing video details: %s", str(e))
            logger.error(traceback.format_exc())
            return None
