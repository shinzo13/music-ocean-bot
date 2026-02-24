import io
import json
import re
import time
from typing import BinaryIO, Optional

from aiohttp import ClientSession
from pytubefix import AsyncYouTube

from app.config.log import get_logger
from app.modules.musicocean.engines.youtube.constants import HEADERS, YTM_DOMAIN, YTM_BASE_API
from app.modules.musicocean.engines.youtube.enums.api_method import YoutubeAPIMethod
from app.modules.musicocean.engines.youtube.models.youtube_track import YoutubeTrack
from app.modules.musicocean.engines.youtube.models.youtube_track_preview import YoutubeTrackPreview
from app.modules.musicocean.engines.youtube.utils import initialize_context
from app.modules.musicocean.engines.youtube.utils.convert_to_mp3 import convert_to_mp3
from app.modules.musicocean.engines.youtube.utils.parsers.parse_search_response import parse_search_response
from app.modules.musicocean.enums import Engine
from app.modules.musicocean.utils import write_id3

logger = get_logger(__name__)

class YoutubeClient:
    session: ClientSession | None

    def __init__(self):
        self.session = None
        self.context = None

    async def _get_visitor_id(self) -> str:
        if not self.session:
            raise RuntimeError("youtube is uninitialized")

        async with self.session.get(YTM_DOMAIN) as resp:
            text = await resp.text()

        matches = re.findall(r"ytcfg\.set\s*\(\s*({.+?})\s*\)\s*;", text)
        if not matches:
            raise RuntimeError("cant fetch visitor id")
        visitor_id = json.loads(matches[0]).get("VISITOR_DATA")
        if not visitor_id:
            raise RuntimeError("cant fetch visitor id")
        return visitor_id

    async def setup(self):
        self.context = initialize_context()
        self.session = ClientSession(
            cookies = {"SOCS": "CAI"},
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

    async def search_tracks(self, query: str, ignore_spelling=True):
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
                artist_name=raw_track.get("artist","?"),
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


    async def download_track(
            self,
            track_id: str,
            watermark: Optional[str] = None
    ):
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
        stream = await yt.get_stream_by_itag(251)
        data = io.BytesIO()
        stream.stream_to_buffer(data)
        data.seek(0)
        track.content = data.read()
        # content = convert_to_mp3(data.read())
        # logger.debug(f"DATA LEN: {len(content)}")
        # track.content = await write_id3(
        #     track=track,
        #     source=content,
        #     engine=Engine.YOUTUBE,
        #     watermark=watermark,
        #     convert_to_mp3=True
        # )

        return track
