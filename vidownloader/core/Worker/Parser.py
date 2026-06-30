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

        _RENDERER_ = "lockupViewModel" if is_videos else "shortsLockupViewModel"
        _ID_ = "contentId" if is_videos else "entityId"
        _TITLE = "metadata" if is_videos else "overlayMetadata"

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
                    title = title_["lockupMetadataViewModel"]["title"]["content"]
                else:
                    title = title_["primaryText"]["content"]

                video_id = renderer[_ID_]
                if not is_videos:
                    video_id = video_id.replace("shorts-shelf-item-", "")

                # Extract duration if available
                duration = None
                if is_videos:
                    duration = renderer.get("lengthText", {}).get("simpleText", "")

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

            if not playlist_owner:
                try:
                    header = data.get("header", {})
                    page_header = header.get("pageHeaderRenderer", {})
                    content = page_header.get("content", {})
                    vm = content.get("pageHeaderViewModel", {})
                    meta = vm.get("metadata", {}).get("contentMetadataViewModel", {})
                    rows = meta.get("metadataRows", [])
                    if rows:
                        parts = rows[0].get("metadataParts", [])
                        if parts:
                            avatar_stack = parts[0].get("avatarStack", {})
                            vm_text = avatar_stack.get("avatarStackViewModel", {}).get(
                                "text", {}
                            )
                            owner_str = vm_text.get("content", "")
                            if owner_str:
                                if owner_str.startswith("by "):
                                    playlist_owner = owner_str[3:]
                                else:
                                    playlist_owner = owner_str
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
                        if "continuationItemRenderer" in section:
                            continuation_token = Parser._extract_continuation_token(
                                section
                            )
                        elif "itemSectionRenderer" in section:
                            raw_content_list = section.get(
                                "itemSectionRenderer", {}
                            ).get("contents", [])
                            # Token is INSIDE the playlist contents as the LAST item
                            if raw_content_list:
                                last_item = raw_content_list[-1]
                                if "continuationItemRenderer" in last_item:
                                    continuation_token = (
                                        Parser._extract_continuation_token(last_item)
                                    )

            # Extract from nested richGridRenderer if present (e.g. playlist of Shorts)
            if raw_content_list and len(raw_content_list) > 0:
                first_item = raw_content_list[0]
                if "richGridRenderer" in first_item:
                    raw_content_list = first_item["richGridRenderer"].get(
                        "contents", []
                    )

            if not raw_content_list:
                logger.debug("No raw_content_list found in playlist response")
                return videos, continuation_token

            logger.debug(
                f"Found {len(raw_content_list)} items in raw_content_list, continuation_token: {continuation_token[:50] if continuation_token else None}..."
            )

            for content in raw_content_list:
                # If wrapped in richItemRenderer (as in richGridRenderer grids)
                if "richItemRenderer" in content:
                    content = content["richItemRenderer"].get("content", {})

                renderer = content.get("lockupViewModel") or content.get(
                    "shortsLockupViewModel"
                )
                if not renderer:
                    continue

                video_id = renderer.get("contentId") or renderer.get("entityId")
                if not video_id:
                    continue

                if video_id.startswith("shorts-shelf-item-"):
                    video_id = video_id.replace("shorts-shelf-item-", "")

                title = ""
                uploader = ""

                # Extract title and uploader based on renderer type
                if "shortsLockupViewModel" in content:
                    # Shorts
                    title = (
                        renderer.get("overlayMetadata", {})
                        .get("primaryText", {})
                        .get("content", "")
                    )
                else:
                    # Videos
                    metadata = renderer.get("metadata", {}).get(
                        "lockupMetadataViewModel"
                    )
                    if metadata:
                        title = metadata.get("title", {}).get("content", "")
                        try:
                            uploader = (
                                metadata.get("metadata", {})
                                .get("contentMetadataViewModel", {})
                                .get("metadataRows", [])[0]
                                .get("metadataParts", [])[0]
                                .get("text", {})
                                .get("content")
                            )
                        except (IndexError, KeyError, TypeError, AttributeError):
                            uploader = ""

                # Fallback: If uploader not found, use playlist owner
                if not uploader and playlist_owner:
                    uploader = playlist_owner

                # Extract duration (eg. 1:05:14)
                duration = None
                content_image = renderer.get("contentImage", {})
                if content_image:
                    try:
                        duration = (
                            content_image.get("thumbnailViewModel", {})
                            .get("overlays", [])[0]
                            .get("thumbnailBottomOverlayViewModel", {})
                            .get("badges", [])[0]
                            .get("thumbnailBadgeViewModel", {})
                            .get("text", "")
                        )
                    except (IndexError, KeyError, TypeError):
                        duration = None

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
            duration = video_renderer.get("lengthSeconds")

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
