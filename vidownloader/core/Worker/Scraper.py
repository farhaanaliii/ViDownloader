import traceback

from PyQt5.QtCore import QObject, pyqtSignal

from vidownloader.core import Logger, http
from vidownloader.core.Constants import EventType, VideoType, YouTube
from vidownloader.core.Models import Link, ScraperEvent, Video
from vidownloader.core.Worker.Parser import Parser

logger = Logger.get_logger("Scraper")


class Scraper(QObject):
    _event = pyqtSignal(ScraperEvent)
    stop_signal = False

    def __init__(self, link: Link):
        super().__init__()
        self.link = link

    def start(self):
        logger.debug(f"Starting scraper for link: {self.link}")

        if (
            self.link.username or self.link.channel_id
        ):  # if username or channel id exists then we'll scrap the channel
            channel_id = self.link.channel_id or self._get_channel_id()
            self._scrape_channel(channel_id, self.link.video_type)
        elif self.link.playlist_id:
            self._scrape_playlist(self.link.playlist_id)
        elif self.link.video_id:
            self._scrape_video(self.link.video_id)

    def _scrape_channel(self, channel_id: str, video_type: VideoType):
        logger.debug(f"Scraping {video_type} for channel_id: {channel_id}")
        continuation_token = None
        videos_count = 0

        while not self.stop_signal:
            data = {
                "browseId": channel_id,
                "params": (
                    YouTube.VIDEOS_PARAMS
                    if video_type == VideoType.VIDEO
                    else YouTube.SHORTS_PARAMS
                ),
            }

            if continuation_token:
                data["continuation"] = continuation_token

            response = self._call_api(data, "browse")
            if not response:
                logger.error("Failed to retrieve data from YouTube API.")
                break

            videos, continuation_token = (
                Parser.parse_channel_videos_or_shorts_and_token(
                    response, video_type, self.link.username
                )
            )
            self.emit_videos(videos)
            videos_count += len(videos)
            logger.debug(
                f"Scraped {len(videos)} {video_type}, total so far: {videos_count}"
            )

            if not continuation_token:
                break

        logger.debug(f"Scraping completed. Total {video_type} found: {videos_count}")

    def _get_channel_id(self):
        try:
            resp = self._call_api({"url": self.link.url}, "navigation/resolve_url")
            return resp["endpoint"]["browseEndpoint"]["browseId"]
        except Exception as e:
            logger.error("Failed to get channel ID: %s", str(e))
            logger.error(traceback.format_exc())
            return None

    def _scrape_playlist(self, playlist_id: str):
        logger.debug(f"Scraping playlist_id: {playlist_id}")
        continuation_token = None
        videos_count = 0
        playlist_name = None

        while not self.stop_signal:
            if continuation_token:
                data = {"continuation": continuation_token}
            else:
                data = {"browseId": f"VL{playlist_id}"}

            response = self._call_api(data, "browse")
            if not response:
                logger.error("Failed to retrieve data from YouTube API.")
                break

            # Extract playlist name from first response
            if playlist_name is None:
                playlist_name = Parser.extract_playlist_name(response)
                if playlist_name:
                    logger.debug(f"Extracted playlist name: {playlist_name}")
                    # Update link with playlist name
                    if self.link:
                        self.link.playlist_name = playlist_name

            videos, continuation_token = Parser.parse_playlist_videos_and_token(
                response
            )

            if not videos:
                logger.debug("No videos found in response, stopping.")
                break

            # Set playlist metadata on all videos
            for video in videos:
                video.playlist_id = playlist_id
                video.playlist_name = playlist_name

            self.emit_videos(videos)
            videos_count += len(videos)
            logger.debug(
                f"Scraped {len(videos)} videos from playlist, total so far: {videos_count}"
            )

            if not continuation_token:
                break

        logger.debug(
            f"Scraping completed. Total videos found in playlist: {videos_count}"
        )

    def _scrape_video(self, video_id: str):
        logger.debug(f"Scraping video_id: {video_id}")
        data = {"videoId": video_id}
        response = self._call_api(data, "player")
        if not response:
            logger.error("Failed to retrieve data from YouTube API.")
            return

        video = Parser.parse_video_details(response)
        if video:
            self.emit_videos([video])
            logger.debug(f"Scraped video: {video.caption} ({video.video_id})")

    def set_stop(self):
        self.stop_signal = True

    def emit_message(self, message: str):
        self._event.emit(ScraperEvent(event=EventType.MESSAGE, message=message))

    def emit_videos(self, videos: list[Video]):
        self._event.emit(ScraperEvent(event=EventType.VIDEOS, videos=videos))

    def _call_api(self, data: dict, r_type: str):
        _data = {
            "context": {
                "client": {
                    "hl": "en",
                    "gl": "US",
                    "deviceMake": "",
                    "deviceModel": "",
                    "visitorData": "CgsyX0p2ZnFrdTI2Zyjp_8TKBjIKCgJQSxIEGgAgamLfAgrcAjE0LllUPUFVR195ZFBxYllXYVo2Vmt4OHVEZjVFdldZSVVtYTNiLW9mUzZ3b0lRUW83cVFkTXU2S2V3RTY5UC1tUjBMREphUzBWYlpQeDlyQXpqMjF0aFF0TUdBS0JnZDFlMXNvUU9CbXRTbzl6Um96Skp5ZEdmOFFLQlE1V2V4c2pJYkRjRHVhdFlQU081WUV1TWtuVFdleGptaG1UbUVKeGN4aUVQMHpUdnVSTjVKQzFqOHpKMHBPU1p1OGxlaXhxWkk1LUNVcVFDNmpGMnpfWjVXLVhDOGs5SGUwMGZ4cFdvVTU0RFNaeF9iS29lVnowYTJtZU9tLWJMeEY3Z3NPTTVzNG45cG1uQkxIcHhybVBaQVhZN1lQRjhoRjFYaFF5Z3ZjampuMGVGOGxBdXh2OGZoTTNQQ3NPOG83Z1RzSWZvdXFVLTJ4eGJKb0RVZmVrdExYMW9GRDM0QQ%3D%3D",
                    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36,gzip(gfe)",
                    "clientName": "WEB",
                    "clientVersion": "2.20251222.04.00",
                    "osName": "Windows",
                    "osVersion": "10.0",
                    "screenPixelDensity": 1,
                    "platform": "DESKTOP",
                    "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                    "screenDensityFloat": 1,
                    "browserName": "Chrome",
                    "browserVersion": "143.0.0.0",
                    "acceptHeader": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "deviceExperimentId": "ChxOelU0T0RreE56RXhOekE0TWpnNE5EYzNNQT09EOn_xMoGGOn_xMoG",
                    "screenWidthPoints": 1263,
                    "screenHeightPoints": 919,
                    "utcOffsetMinutes": 300,
                    "userInterfaceTheme": "USER_INTERFACE_THEME_LIGHT",
                    "memoryTotalKbytes": "8000000",
                    "connectionType": "CONN_CELLULAR_4G",
                    "mainAppWebInfo": {
                        "webDisplayMode": "WEB_DISPLAY_MODE_BROWSER",
                        "isWebNativeShareAvailable": True,
                        "pwaInstallabilityStatus": "PWA_INSTALLABILITY_STATUS_CAN_BE_INSTALLED",
                    },
                },
                "user": {
                    "lockedSafetyMode": False,
                },
                "request": {
                    "useSsl": True,
                    "internalExperimentFlags": [],
                    "consistencyTokenJars": [],
                },
            },
            **data,
        }

        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "x-youtube-client-name": "1",
            "x-youtube-client-version": "2.20251222.04.00",
            "x-origin": "https://www.youtube.com",
            "device-memory": "8",
            "sec-ch-dpr": "1",
            "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            "sec-ch-ua-arch": '"x86"',
            "sec-ch-ua-bitness": '"64"',
            "sec-ch-ua-form-factors": '"Desktop"',
            "sec-ch-ua-full-version": '"143.0.7499.170"',
            "sec-ch-ua-full-version-list": '"Google Chrome";v="143.0.7499.170", "Chromium";v="143.0.7499.170", "Not A(Brand";v="24.0.0.0"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": '""',
            "sec-ch-ua-platform": '"Windows"',
            "sec-ch-ua-platform-version": '"10.0.0"',
            "sec-ch-ua-wow64": "?0",
            "sec-ch-viewport-width": "1263",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "same-origin",
            "sec-fetch-site": "same-origin",
            "x-browser-channel": "stable",
            "x-browser-copyright": "Copyright 2025 Google LLC. All Rights reserved.",
            "x-browser-validation": "UujAs0GAwdnCJ9nvrswZ+O+oco0=",
            "x-browser-year": "2025",
            "x-client-data": "CJDuygE=",
        }

        params = {"prettyPrint": "false"}

        resp_json = None
        try:
            resp_json = http.post(
                f"{YouTube.API}/{r_type}",
                params=params,
                headers=headers,
                json_data=_data,
            ).json()
            return resp_json
        except:
            logger.error("YouTube API call failed for type: %s", r_type)
            logger.error(traceback.format_exc())
            return None
