import json
import re
from typing import Optional
from urllib.parse import parse_qs, unquote

from aiohttp import ClientSession

from app.config.log import get_logger
from app.modules.musicocean.engines.shared.base_client import BaseEngineClient
from app.modules.musicocean.engines.youtube.constants import HEADERS, YTM_DOMAIN, YTM_BASE_API
from app.modules.musicocean.engines.youtube.enums.api_method import YoutubeAPIMethod
from app.modules.musicocean.engines.youtube.exceptions import YouTubeAuthException
from app.modules.musicocean.engines.youtube.models.youtube_album import YoutubeAlbum
from app.modules.musicocean.engines.youtube.models.youtube_artist import YoutubeArtist
from app.modules.musicocean.engines.youtube.models.youtube_playlist import YoutubePlaylist
from app.modules.musicocean.engines.youtube.models.youtube_track import YoutubeTrack
from app.modules.musicocean.engines.youtube.models.youtube_track_preview import YoutubeTrackPreview
from app.modules.musicocean.engines.youtube.utils import initialize_context
from app.modules.musicocean.engines.youtube.utils.parsers.parse_search_response import parse_search_response
from app.modules.musicocean.utils.id3 import write_mp4_tags

logger = get_logger(__name__)


class YoutubeClient(BaseEngineClient):
    session: ClientSession | None

    def __init__(self):
        self.session = None
        self.context = None

    async def _get_visitor_id(self) -> str:
        async with self.session.get(YTM_DOMAIN) as resp:
            text = await resp.text()

        matches = re.findall(r"ytcfg\.set\s*\(\s*({.+?})\s*\)\s*;", text)
        if not matches:
            raise YouTubeAuthException("Cant fetch visitor id")
        visitor_id = json.loads(matches[0]).get("VISITOR_DATA")
        if not visitor_id:
            raise YouTubeAuthException("Cant fetch visitor id")
        return visitor_id

    async def setup(self):
        self.context = initialize_context()
        self.session = ClientSession(
            cookies={"SOCS": "CAI"},
            headers=HEADERS,
        )
        visitor_id = await self._get_visitor_id()
        self.session.headers["X-Goog-Visitor-Id"] = visitor_id

    async def _api_request(
            self,
            method: YoutubeAPIMethod,
            payload: dict,
    ) -> dict:
        payload.update(self.context)
        async with self.session.post(
                f"{YTM_BASE_API}/{method}?alt=json",
                json=payload
        ) as resp:
            resp.raise_for_status()
            raw_data = await resp.json()
            return raw_data

    async def _get_video_info(self, video_id: str) -> dict:
        url = f"https://www.youtube.com/watch?v={video_id}"
        async with self.session.get(url) as resp:
            resp.raise_for_status()
            html = await resp.text()

        match = re.search(r'var ytInitialPlayerResponse\s*=\s*({.+?});', html)
        if not match:
            raise YouTubeAuthException(f"Cannot extract player response for video {video_id}")

        player_response = json.loads(match.group(1))
        return player_response

    def _extract_video_metadata(self, player_response: dict) -> dict:
        video_details = player_response.get("videoDetails", {})
        return {
            "video_id": video_details.get("videoId"),
            "title": video_details.get("title"),
            "author": video_details.get("author"),
            "length_seconds": int(video_details.get("lengthSeconds", 0)),
            "thumbnail": video_details.get("thumbnail", {}).get("thumbnails", [{}])[-1].get("url"),
        }

    def _get_audio_stream_url(self, player_response: dict) -> Optional[str]:
        streaming_data = player_response.get("streamingData", {})
        formats = streaming_data.get("adaptiveFormats", [])

        for fmt in formats:
            if fmt.get("itag") == 140:
                url = fmt.get("url")
                if url:
                    return url

                cipher = fmt.get("signatureCipher") or fmt.get("cipher")
                if cipher:
                    params = parse_qs(cipher)
                    url = params.get("url", [None])[0]
                    if url:
                        return unquote(url)

        return None

    async def get_track(self, track_id: str) -> YoutubeTrackPreview:
        player_response = await self._get_video_info(track_id)
        metadata = self._extract_video_metadata(player_response)

        return YoutubeTrackPreview(
            id=track_id,
            title=metadata["title"],
            artist_name=metadata["author"].removesuffix(" - Topic"),
            cover_url=metadata["thumbnail"]
        )

    async def search_tracks(
            self,
            query: str,
            ignore_spelling=True
    ) -> list[YoutubeTrackPreview]:
        raw_data = await self._api_request(
            YoutubeAPIMethod.SEARCH,
            {
                "query": query,
                "params":
                    "EgWKAQIYAUICCAFqDBAOEAoQAxAEEAkQBQ%3D%3D"
                    if not ignore_spelling else
                    "EgWKAQIIAWoMEA4QChADEAQQCRAF"
            }
        )

        if "contents" not in raw_data:
            return []

        raw_tracks = parse_search_response(raw_data)

        tracks = [
            YoutubeTrackPreview(
                id=raw_track.get("video_id"),
                title=raw_track.get("title"),
                artist_name=raw_track.get("artist", "?"),
                cover_url=raw_track.get("thumbnail")
            )
            for raw_track in raw_tracks
        ]

        return tracks

    async def search_exact_match(self, title: str, artist: str):
        matches = await self.search_tracks(
            f'{title} {artist}',
            ignore_spelling=True
        )
        if not matches:
            return None
        return matches[0]

    async def search_albums(self, query: str) -> list[YoutubeAlbum]:
        raw_data = await self._api_request(
            YoutubeAPIMethod.SEARCH,
            {
                "query": query,
                "params": "EgWKAQIYAWoMEA4QChADEAQQCRAF"
            }
        )

        if "contents" not in raw_data:
            return []

        albums = []
        try:
            tabs = raw_data["contents"]["tabbedSearchResultsRenderer"]["tabs"]
            for tab in tabs:
                if "tabRenderer" in tab and tab["tabRenderer"].get("selected", False):
                    sections = tab["tabRenderer"]["content"]["sectionListRenderer"]["contents"]
                    for section in sections:
                        if "musicShelfRenderer" in section:
                            shelf = section["musicShelfRenderer"]
                            title_text = shelf.get("title", {}).get("runs", [{}])[0].get("text", "")
                            if title_text == "Albums":
                                for item in shelf.get("contents", []):
                                    if "musicResponsiveListItemRenderer" in item:
                                        renderer = item["musicResponsiveListItemRenderer"]
                                        album_id = renderer.get("navigationEndpoint", {}).get("browseEndpoint", {}).get("browseId")
                                        flex_columns = renderer.get("flexColumns", [])

                                        title = ""
                                        artist_name = ""

                                        if len(flex_columns) > 0:
                                            title = flex_columns[0].get("musicResponsiveListItemFlexColumnRenderer", {}).get("text", {}).get("runs", [{}])[0].get("text", "")

                                        if len(flex_columns) > 1:
                                            runs = flex_columns[1].get("musicResponsiveListItemFlexColumnRenderer", {}).get("text", {}).get("runs", [])
                                            if len(runs) > 0:
                                                artist_name = runs[0].get("text", "")

                                        thumbnail = renderer.get("thumbnail", {}).get("musicThumbnailRenderer", {}).get("thumbnail", {}).get("thumbnails", [{}])[-1].get("url", "")

                                        if album_id:
                                            albums.append(YoutubeAlbum(
                                                id=album_id,
                                                title=title,
                                                artist_name=artist_name,
                                                cover_url=thumbnail
                                            ))
        except (KeyError, IndexError):
            pass

        return albums

    async def search_playlists(self, query: str) -> list[YoutubePlaylist]:
        raw_data = await self._api_request(
            YoutubeAPIMethod.SEARCH,
            {
                "query": query,
                "params": "EgWKAQIoAWoMEA4QChADEAQQCRAF"
            }
        )

        if "contents" not in raw_data:
            return []

        playlists = []
        try:
            tabs = raw_data["contents"]["tabbedSearchResultsRenderer"]["tabs"]
            for tab in tabs:
                if "tabRenderer" in tab and tab["tabRenderer"].get("selected", False):
                    sections = tab["tabRenderer"]["content"]["sectionListRenderer"]["contents"]
                    for section in sections:
                        if "musicShelfRenderer" in section:
                            shelf = section["musicShelfRenderer"]
                            title_text = shelf.get("title", {}).get("runs", [{}])[0].get("text", "")
                            if title_text == "Community playlists":
                                for item in shelf.get("contents", []):
                                    if "musicResponsiveListItemRenderer" in item:
                                        renderer = item["musicResponsiveListItemRenderer"]
                                        playlist_id = renderer.get("navigationEndpoint", {}).get("browseEndpoint", {}).get("browseId")
                                        flex_columns = renderer.get("flexColumns", [])

                                        title = ""
                                        if len(flex_columns) > 0:
                                            title = flex_columns[0].get("musicResponsiveListItemFlexColumnRenderer", {}).get("text", {}).get("runs", [{}])[0].get("text", "")

                                        thumbnail = renderer.get("thumbnail", {}).get("musicThumbnailRenderer", {}).get("thumbnail", {}).get("thumbnails", [{}])[-1].get("url", "")

                                        if playlist_id:
                                            playlists.append(YoutubePlaylist(
                                                id=playlist_id,
                                                title=title,
                                                cover_url=thumbnail,
                                                track_count=0
                                            ))
        except (KeyError, IndexError):
            pass

        return playlists

    async def search_artists(self, query: str) -> list[YoutubeArtist]:
        raw_data = await self._api_request(
            YoutubeAPIMethod.SEARCH,
            {
                "query": query,
                "params": "EgWKAQIgAWoMEA4QChADEAQQCRAF"
            }
        )

        if "contents" not in raw_data:
            return []

        artists = []
        try:
            tabs = raw_data["contents"]["tabbedSearchResultsRenderer"]["tabs"]
            for tab in tabs:
                if "tabRenderer" in tab and tab["tabRenderer"].get("selected", False):
                    sections = tab["tabRenderer"]["content"]["sectionListRenderer"]["contents"]
                    for section in sections:
                        if "musicShelfRenderer" in section:
                            shelf = section["musicShelfRenderer"]
                            title_text = shelf.get("title", {}).get("runs", [{}])[0].get("text", "")
                            if title_text == "Artists":
                                for item in shelf.get("contents", []):
                                    if "musicResponsiveListItemRenderer" in item:
                                        renderer = item["musicResponsiveListItemRenderer"]
                                        artist_id = renderer.get("navigationEndpoint", {}).get("browseEndpoint", {}).get("browseId")
                                        flex_columns = renderer.get("flexColumns", [])

                                        name = ""
                                        if len(flex_columns) > 0:
                                            name = flex_columns[0].get("musicResponsiveListItemFlexColumnRenderer", {}).get("text", {}).get("runs", [{}])[0].get("text", "")

                                        thumbnail = renderer.get("thumbnail", {}).get("musicThumbnailRenderer", {}).get("thumbnail", {}).get("thumbnails", [{}])[-1].get("url", "")

                                        if artist_id:
                                            artists.append(YoutubeArtist(
                                                id=artist_id,
                                                name=name,
                                                photo_url=thumbnail
                                            ))
        except (KeyError, IndexError):
            pass

        return artists

    async def _browse(self, browse_id: str) -> dict:
        raw_data = await self._api_request(
            YoutubeAPIMethod.BROWSE,
            {"browseId": browse_id}
        )
        return raw_data

    def _parse_track_from_renderer(self, renderer: dict) -> Optional[YoutubeTrackPreview]:
        try:
            video_id = renderer.get("playlistItemData", {}).get("videoId")
            if not video_id:
                return None

            flex_columns = renderer.get("flexColumns", [])

            title = ""
            artist_name = ""

            if len(flex_columns) > 0:
                title = flex_columns[0].get("musicResponsiveListItemFlexColumnRenderer", {}).get("text", {}).get("runs", [{}])[0].get("text", "")

            if len(flex_columns) > 1:
                runs = flex_columns[1].get("musicResponsiveListItemFlexColumnRenderer", {}).get("text", {}).get("runs", [])
                if len(runs) > 0:
                    artist_name = runs[0].get("text", "")

            thumbnail = renderer.get("thumbnail", {}).get("musicThumbnailRenderer", {}).get("thumbnail", {}).get("thumbnails", [{}])[-1].get("url", "")

            return YoutubeTrackPreview(
                id=video_id,
                title=title,
                artist_name=artist_name,
                cover_url=thumbnail
            )
        except (KeyError, IndexError):
            return None

    async def get_album(self, album_id: str) -> YoutubeAlbum:
        raw_data = await self._browse(album_id)

        header = raw_data.get("header", {}).get("musicDetailHeaderRenderer", {})
        title = header.get("title", {}).get("runs", [{}])[0].get("text", "")
        subtitle_runs = header.get("subtitle", {}).get("runs", [])
        artist_name = subtitle_runs[0].get("text", "") if len(subtitle_runs) > 0 else ""
        thumbnail = header.get("thumbnail", {}).get("croppedSquareThumbnailRenderer", {}).get("thumbnail", {}).get("thumbnails", [{}])[-1].get("url", "")

        return YoutubeAlbum(
            id=album_id,
            title=title,
            artist_name=artist_name,
            cover_url=thumbnail
        )

    async def get_playlist(self, playlist_id: str) -> YoutubePlaylist:
        raw_data = await self._browse(playlist_id)

        header = raw_data.get("header", {}).get("musicDetailHeaderRenderer", {})
        title = header.get("title", {}).get("runs", [{}])[0].get("text", "")
        subtitle_runs = header.get("subtitle", {}).get("runs", [])

        track_count = 0
        for run in subtitle_runs:
            text = run.get("text", "")
            if text.isdigit():
                track_count = int(text)
                break

        thumbnail = header.get("thumbnail", {}).get("croppedSquareThumbnailRenderer", {}).get("thumbnail", {}).get("thumbnails", [{}])[-1].get("url", "")

        return YoutubePlaylist(
            id=playlist_id,
            title=title,
            cover_url=thumbnail,
            track_count=track_count
        )

    async def get_album_tracks(self, album_id: str) -> list[YoutubeTrackPreview]:
        raw_data = await self._browse(album_id)

        tracks = []
        try:
            contents = raw_data.get("contents", {}).get("singleColumnBrowseResultsRenderer", {}).get("tabs", [{}])[0].get("tabRenderer", {}).get("content", {}).get("sectionListRenderer", {}).get("contents", [])

            for section in contents:
                if "musicShelfRenderer" in section:
                    shelf = section["musicShelfRenderer"]
                    for item in shelf.get("contents", []):
                        if "musicResponsiveListItemRenderer" in item:
                            track = self._parse_track_from_renderer(item["musicResponsiveListItemRenderer"])
                            if track:
                                tracks.append(track)
        except (KeyError, IndexError):
            pass

        return tracks

    async def get_artist(self, artist_id: str) -> YoutubeArtist:
        raw_data = await self._browse(artist_id)

        header = raw_data.get("header", {}).get("musicImmersiveHeaderRenderer", {})
        name = header.get("title", {}).get("runs", [{}])[0].get("text", "")
        thumbnail = header.get("thumbnail", {}).get("musicThumbnailRenderer", {}).get("thumbnail", {}).get("thumbnails", [{}])[-1].get("url", "")

        subscribers = None
        subscription_text = header.get("subscriptionButton", {}).get("subscribeButtonRenderer", {}).get("subscriberCountText", {}).get("runs", [{}])[0].get("text", "")
        if subscription_text:
            try:
                if "K" in subscription_text:
                    subscribers = int(float(subscription_text.replace("K", "").strip()) * 1000)
                elif "M" in subscription_text:
                    subscribers = int(float(subscription_text.replace("M", "").strip()) * 1000000)
                else:
                    subscribers = int(subscription_text.replace(",", "").strip())
            except ValueError:
                pass

        return YoutubeArtist(
            id=artist_id,
            name=name,
            photo_url=thumbnail,
            listeners=subscribers
        )

    async def get_artist_tracks(self, artist_id: str) -> list[YoutubeTrackPreview]:
        raw_data = await self._browse(artist_id)

        tracks = []
        try:
            contents = raw_data.get("contents", {}).get("singleColumnBrowseResultsRenderer", {}).get("tabs", [{}])[0].get("tabRenderer", {}).get("content", {}).get("sectionListRenderer", {}).get("contents", [])

            for section in contents:
                if "musicShelfRenderer" in section:
                    shelf = section["musicShelfRenderer"]
                    title_text = shelf.get("title", {}).get("runs", [{}])[0].get("text", "")
                    if title_text in ["Songs", "Top songs"]:
                        for item in shelf.get("contents", []):
                            if "musicResponsiveListItemRenderer" in item:
                                track = self._parse_track_from_renderer(item["musicResponsiveListItemRenderer"])
                                if track:
                                    tracks.append(track)
                        break
        except (KeyError, IndexError):
            pass

        return tracks

    async def get_playlist_tracks(self, playlist_id: str) -> list[YoutubeTrackPreview]:
        raw_data = await self._browse(playlist_id)

        tracks = []
        try:
            contents = raw_data.get("contents", {}).get("singleColumnBrowseResultsRenderer", {}).get("tabs", [{}])[0].get("tabRenderer", {}).get("content", {}).get("sectionListRenderer", {}).get("contents", [])

            for section in contents:
                if "musicPlaylistShelfRenderer" in section:
                    shelf = section["musicPlaylistShelfRenderer"]
                    for item in shelf.get("contents", []):
                        if "musicResponsiveListItemRenderer" in item:
                            track = self._parse_track_from_renderer(item["musicResponsiveListItemRenderer"])
                            if track:
                                tracks.append(track)
        except (KeyError, IndexError):
            pass

        return tracks

    async def download_track(
            self,
            track_id: str,
            watermark: Optional[str] = None
    ) -> YoutubeTrack:
        player_response = await self._get_video_info(track_id)
        metadata = self._extract_video_metadata(player_response)

        cover_url = metadata["thumbnail"]
        async with self.session.get(cover_url) as resp:
            cover = await resp.read()

        track = YoutubeTrack(
            id=track_id,
            title=metadata["title"],
            artist_name=metadata["author"].removesuffix(" - Topic"),
            cover_url=cover_url,
            duration=metadata["length_seconds"],
            cover=cover
        )

        logger.debug("yt: downloading")
        stream_url = self._get_audio_stream_url(player_response)
        if not stream_url:
            raise YouTubeAuthException(f"Cannot find audio stream for video {track_id}")

        async with self.session.get(stream_url) as resp:
            resp.raise_for_status()
            raw = await resp.read()

        logger.debug("yt: writing id3")
        track.content = write_mp4_tags(track, raw, watermark)
        logger.debug("yt: finished")
        return track

    async def close(self):
        if self.session:
            await self.session.close()
