import asyncio
import io
import json
import re
from typing import Optional

from aiohttp import ClientSession
from pytubefix import AsyncYouTube

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
            # ...
            return raw_data

    async def get_track(self, track_id: str) -> YoutubeTrackPreview:
        yt = AsyncYouTube.from_id(track_id)
        return YoutubeTrackPreview(
            id=track_id,
            title=await yt.title(),
            artist_name=(await yt.author()).removesuffix(' - Topic'),
            cover_url=await yt.thumbnail_url()
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
        pass

    async def search_playlists(self, query: str) -> list[YoutubePlaylist]:
        pass

    async def search_artists(self, query: str) -> list[YoutubeArtist]:
        pass

    async def get_album(self, album_id: int):
        pass

    async def get_playlist(self, playlist_id: int):
        pass

    async def get_album_tracks(self, album_id: int):
        pass

    async def get_artist(self, artist_id: int):
        pass

    async def get_artist_tracks(self, artist_id: int):
        pass

    async def get_playlist_tracks(self, playlist_id: int):
        pass

    async def download_track(
            self,
            track_id: str,
            watermark: Optional[str] = None
    ) -> YoutubeTrack:
        yt = AsyncYouTube.from_id(track_id)
        cover_url = await yt.thumbnail_url()
        async with self.session.get(cover_url) as resp:
            cover = await resp.read()
        track = YoutubeTrack(
            id=track_id,
            title=await yt.title(),
            artist_name=(await yt.author()).removesuffix(' - Topic'),
            cover_url=cover_url,
            duration=await yt.length(),
            cover=cover
        )
        logger.debug("yt: downloading")
        stream = await yt.get_stream_by_itag(140)
        data = io.BytesIO()
        # blocking download + cpu-heavy transcode must not starve the event loop
        await asyncio.to_thread(stream.stream_to_buffer, data)
        data.seek(0)
        raw = data.read()
        logger.debug("yt: writing id3")
        track.content = await asyncio.to_thread(write_mp4_tags, track, raw, watermark)
        logger.debug("yt: finished")
        return track

    async def close(self):
        pass
