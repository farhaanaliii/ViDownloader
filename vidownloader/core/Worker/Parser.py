import re
import traceback

from vidownloader.core import Logger
from vidownloader.core.Constants import VideoType
from vidownloader.core.Models import Video
from vidownloader.core.Utils import format_view_count

logger = Logger.get_logger("Parser")


class Parser:

    @staticmethod
    def _extract_continuation_items(data: dict) -> list[dict] | None:
        for action in data.get("onResponseReceivedActions", []):
            if "appendContinuationItemsAction" in action:
                return action["appendContinuationItemsAction"].get("continuationItems")
        return None

    @staticmethod
    def _extract_continuation_token(continuation_item: dict) -> str | None:
        endpoint = continuation_item.get("continuationItemRenderer", {}).get("continuationEndpoint", {})
        cmd = endpoint.get("continuationCommand")
        if cmd and "token" in cmd:
            return cmd["token"]
        for exec_cmd in endpoint.get("commandExecutorCommand", {}).get("commands", []):
            token = exec_cmd.get("continuationCommand", {}).get("token")
            if token:
                return token
        return None

    @staticmethod
    def _extract_playlist_owner(data: dict) -> str | None:
        try:
            microformat = data.get("microformat", {})
            owner = microformat.get("microformatDataRenderer", {}).get("courseDetails", {}).get("providerName")
            if owner:
                return owner

            rows = (
                data.get("header", {})
                .get("pageHeaderRenderer", {})
                .get("content", {})
                .get("pageHeaderViewModel", {})
                .get("metadata", {})
                .get("contentMetadataViewModel", {})
                .get("metadataRows", [])
            )
            if rows:
                owner_str = (
                    rows[0]
                    .get("metadataParts", [{}])[0]
                    .get("avatarStack", {})
                    .get("avatarStackViewModel", {})
                    .get("text", {})
                    .get("content", "")
                )
                if owner_str:
                    return owner_str.removeprefix("by ")
        except Exception:
            pass
        return None

    @staticmethod
    def _parse_video_item(
        content: dict,
        default_username: str = "",
        video_type: VideoType | None = None,
    ) -> Video | None:
        if "richItemRenderer" in content:
            content = content["richItemRenderer"].get("content", {})

        renderer = content.get("lockupViewModel") or content.get("shortsLockupViewModel")
        if not renderer:
            return None

        raw_id = renderer.get("contentId") or renderer.get("entityId")
        if not raw_id:
            return None

        video_id = raw_id.removeprefix("shorts-shelf-item-")
        is_short = "shortsLockupViewModel" in content or (video_type == VideoType.SHORT)
        resolved_type = VideoType.SHORT if is_short else (video_type or VideoType.VIDEO)

        if is_short:
            title = renderer.get("overlayMetadata", {}).get("primaryText", {}).get("content", "")
            uploader = default_username
            duration = None
            views = renderer.get("overlayMetadata", {}).get("secondaryText", {}).get("content")
        else:
            meta = renderer.get("metadata", {}).get("lockupMetadataViewModel", {})
            title = meta.get("title", {}).get("content", "")
            views = None
            uploader = default_username

            rows = meta.get("metadata", {}).get("contentMetadataViewModel", {}).get("metadataRows", [])
            for row in rows:
                for part in row.get("metadataParts", []):
                    text = part.get("text", {}).get("content", "")
                    if not text:
                        continue
                    if re.search(r"\b(views|view|watching|streamed)\b", text, re.IGNORECASE):
                        views = views or text
                    elif not uploader and not re.search(r"\bago\b", text, re.IGNORECASE):
                        uploader = text

            length_text = renderer.get("lengthText", {}).get("simpleText")
            try:
                badge_text = (
                    renderer.get("contentImage", {})
                    .get("thumbnailViewModel", {})
                    .get("overlays", [])[0]
                    .get("thumbnailBottomOverlayViewModel", {})
                    .get("badges", [])[0]
                    .get("thumbnailBadgeViewModel", {})
                    .get("text")
                )
            except (IndexError, KeyError, TypeError):
                badge_text = None
            duration = length_text or badge_text or None

        url = (
            f"https://www.youtube.com/shorts/{video_id}"
            if resolved_type == VideoType.SHORT
            else f"https://www.youtube.com/watch?v={video_id}"
        )

        return Video(
            caption=title,
            username=uploader,
            video_id=video_id,
            _type=resolved_type,
            url=url,
            duration=duration,
            views=views,
        )

    @staticmethod
    def extract_channel_name(data: dict) -> str | None:
        try:
            header = data.get("header", {})
            page_header = header.get("pageHeaderRenderer", {}).get("content", {}).get("pageHeaderViewModel", {})
            if title := page_header.get("title", {}).get("dynamicTextViewModel", {}).get("text", {}).get("content"):
                return title

            c4 = header.get("c4TabbedHeaderRenderer", {})
            if title := c4.get("title"):
                return title

            meta = data.get("metadata", {}).get("channelMetadataRenderer", {})
            if title := meta.get("title"):
                return title

            micro = data.get("microformat", {}).get("microformatDataRenderer", {})
            if title := micro.get("title"):
                return title
        except Exception as e:
            logger.debug(f"Error extracting channel name: {e}")
        return None

    @staticmethod
    def parse_channel_videos_or_shorts_and_token(
        data: dict, video_type: VideoType, username: str
    ) -> tuple[list[Video], str | None]:
        videos = []
        continuation_token = None

        try:
            if not username:
                username = Parser.extract_channel_name(data) or ""
            raw_content_list = Parser._extract_continuation_items(data)
            if raw_content_list is None:
                tabs = data.get("contents", {}).get("twoColumnBrowseResultsRenderer", {}).get("tabs", [])
                target_tab = None
                for tab in tabs:
                    renderer = tab.get("tabRenderer", {})
                    if renderer.get("title") == video_type.capitalize():
                        target_tab = renderer
                        break

                if not target_tab:
                    return [], None

                raw_content_list = target_tab.get("content", {}).get("richGridRenderer", {}).get("contents", [])

            if not raw_content_list:
                return [], None

            for content in raw_content_list:
                if token := Parser._extract_continuation_token(content):
                    continuation_token = token
                    continue

                if video := Parser._parse_video_item(content, default_username=username, video_type=video_type):
                    videos.append(video)

            return videos, continuation_token
        except Exception as e:
            logger.error("Error parsing channel videos: %s", str(e))
            logger.error(traceback.format_exc())
            return videos, continuation_token

    @staticmethod
    def extract_playlist_name(data: dict) -> str | None:
        try:
            header = data.get("header", {}).get("pageHeaderRenderer", {})
            title = header.get("pageTitle")
            if not title:
                metadata = data.get("metadata", {}).get("playlistMetadataRenderer", {})
                title = metadata.get("title")
            return title
        except Exception as e:
            logger.debug(f"Error extracting playlist name: {e}")
            return None

    @staticmethod
    def parse_playlist_videos_and_token(data: dict) -> tuple[list[Video], str | None]:
        videos = []
        continuation_token = None

        try:
            playlist_owner = Parser._extract_playlist_owner(data) or ""
            raw_content_list = Parser._extract_continuation_items(data)

            if raw_content_list is not None:
                for content in reversed(raw_content_list):
                    if token := Parser._extract_continuation_token(content):
                        continuation_token = token
                        break
            else:
                tabs = data.get("contents", {}).get("twoColumnBrowseResultsRenderer", {}).get("tabs", [])
                for tab in tabs:
                    contents = (
                        tab.get("tabRenderer", {}).get("content", {}).get("sectionListRenderer", {}).get("contents", [])
                    )
                    for section in contents:
                        if token := Parser._extract_continuation_token(section):
                            continuation_token = token
                        elif "itemSectionRenderer" in section:
                            raw_content_list = section["itemSectionRenderer"].get("contents", [])
                            if raw_content_list:
                                if token := Parser._extract_continuation_token(raw_content_list[-1]):
                                    continuation_token = token

            if raw_content_list and "richGridRenderer" in raw_content_list[0]:
                raw_content_list = raw_content_list[0]["richGridRenderer"].get("contents", [])

            if not raw_content_list:
                return videos, continuation_token

            for content in raw_content_list:
                if video := Parser._parse_video_item(content, default_username=playlist_owner):
                    videos.append(video)

            return videos, continuation_token
        except Exception as e:
            logger.error("Error parsing playlist: %s", str(e))
            logger.error(traceback.format_exc())
            return videos, continuation_token

    @staticmethod
    def parse_video_details(data: dict) -> Video | None:
        try:
            details = data.get("videoDetails")
            if not details:
                return None

            video_id = details.get("videoId", "")
            title = details.get("title", "")
            duration = details.get("lengthSeconds")
            raw_views = details.get("viewCount")
            views = format_view_count(raw_views) if raw_views else None

            owner_url = data.get("microformat", {}).get("playerMicroformatRenderer", {}).get("ownerProfileUrl", "")
            username = owner_url.split("/@")[-1].rstrip("/") if "/@" in owner_url else ""

            return Video(
                caption=title,
                username=username,
                video_id=video_id,
                _type=VideoType.VIDEO,
                url=f"https://www.youtube.com/watch?v={video_id}",
                duration=duration,
                views=views,
            )
        except Exception as e:
            logger.error("Error parsing video details: %s", str(e))
            logger.error(traceback.format_exc())
            return None
