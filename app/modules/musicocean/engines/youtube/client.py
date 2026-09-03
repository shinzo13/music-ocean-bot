import asyncio
import json
import re
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional

from aiohttp import ClientSession
from pytubefix import AsyncYouTube
from yt_dlp import YoutubeDL

from app.config.log import get_logger
from app.modules.musicocean.engines.shared.base_client import BaseEngineClient
from app.modules.musicocean.engines.youtube.constants import HEADERS, YTM_DOMAIN, YTM_BASE_API
from app.modules.musicocean.engines.youtube.enums.api_method import YoutubeAPIMethod
from app.modules.musicocean.engines.youtube.exceptions import YouTubeAuthException, YoutubeBlockedException, \
    YoutubeDataException
from app.modules.musicocean.engines.youtube.models.youtube_album import YoutubeAlbum
from app.modules.musicocean.engines.youtube.models.youtube_artist import YoutubeArtist
from app.modules.musicocean.engines.youtube.models.youtube_audio import YoutubeAudio
from app.modules.musicocean.engines.youtube.models.youtube_playlist import YoutubePlaylist
from app.modules.musicocean.engines.youtube.models.youtube_track import YoutubeTrack
from app.modules.musicocean.engines.youtube.models.youtube_track_preview import YoutubeTrackPreview
from app.modules.musicocean.engines.youtube.utils import initialize_context
from app.modules.musicocean.engines.youtube.utils.parsers.parse_search_response import parse_search_response
from app.modules.musicocean.utils.id3 import write_mp4_tags
from app.modules.musicocean.utils.square_cover import square_cover

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

    # youtube answers the same request with a bot check maybe a third of the
    # time, and a different client is usually served without one. Order matters:
    # the first is pytubefix's default, the rest are what still worked when it
    # was refused.
    CLIENTS = ("ANDROID_VR", "WEB_MUSIC", "IOS", "WEB")

    async def _open(self, track_id: str) -> AsyncYouTube:
        """Opens a video, walking through clients until one is not challenged."""
        url = f"https://youtube.com/watch?v={track_id}"
        last: Exception | None = None
        for client in self.CLIENTS:
            yt = AsyncYouTube(url, client=client)
            try:
                # forces the player response: without it the bot check surfaces
                # later, halfway through the download
                await yt.title()
                return yt
            except Exception as e:  # noqa: BLE001 — every client fails its own way
                last = e
                logger.debug(f"yt: {client} refused {track_id}: {type(e).__name__}")
        raise YoutubeDataException(f"no youtube client could open {track_id}: {last!r}")

    async def get_track(self, track_id: str) -> YoutubeTrackPreview:
        yt = await self._open(track_id)
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
        audio, raw = await self._fetch_audio(track_id)

        cover_url = audio.thumbnail_url
        async with self.session.get(
                f"https://i.ytimg.com/vi/{track_id}/maxresdefault.jpg"
        ) as resp:
            if resp.status == 200:
                cover = await resp.read()
            else:
                async with self.session.get(cover_url) as fallback:
                    cover = await fallback.read()
        # yt thumbs are 16:9 with baked-in bars — trim them and crop to square
        cover = await asyncio.to_thread(square_cover, cover)
        track = YoutubeTrack(
            id=track_id,
            title=audio.title,
            artist_name=audio.artist_name.removesuffix(' - Topic'),
            cover_url=cover_url,
            duration=audio.duration,
            cover=cover
        )
        logger.debug("yt: writing id3")
        track.content = await asyncio.to_thread(write_mp4_tags, track, raw, watermark)
        logger.debug("yt: finished")
        return track

    # 140 is the m4a audio track youtube serves for music; the rest is for the
    # occasional upload that has no 140 at all
    AUDIO_FORMAT = "140/bestaudio[ext=m4a]/bestaudio"

    def _download_audio(self, track_id: str) -> tuple[dict, bytes]:
        """Blocking download — call it in a thread."""
        with TemporaryDirectory() as tmp:
            options = {
                "format": self.AUDIO_FORMAT,
                "outtmpl": f"{tmp}/%(id)s.%(ext)s",
                "quiet": True,
                "no_warnings": True,
                "noprogress": True,
                "retries": 3,
            }
            with YoutubeDL(options) as ydl:
                info = ydl.extract_info(
                    f"https://youtube.com/watch?v={track_id}",
                    download=True
                )
                return info, Path(ydl.prepare_filename(info)).read_bytes()

    async def _fetch_audio(self, track_id: str) -> tuple[YoutubeAudio, bytes]:
        """Downloads the audio stream through yt-dlp.

        pytubefix still opens videos fine, but since youtube tightened the
        player it hands out stream urls that die mid-transfer on every one of
        its clients: bot check, 403 or 400 once the bytes start moving. yt-dlp
        keeps up with the player changes, so the download goes through it while
        the metadata calls stay on pytubefix.
        """
        try:
            logger.debug(f"yt: downloading {track_id}")
            info, raw = await asyncio.to_thread(self._download_audio, track_id)
        except Exception as e:  # noqa: BLE001 — yt-dlp raises its own hierarchy
            logger.debug(f"yt: yt-dlp refused {track_id}: {type(e).__name__}")
            raise YoutubeBlockedException(
                track_id,
                f"yt-dlp could not serve {track_id}: {e!r}",
                *(await self._describe(track_id)),
            )

        audio = YoutubeAudio(
            title=info.get("track") or info.get("title") or track_id,
            artist_name=info.get("artist") or info.get("uploader") or "?",
            duration=int(info.get("duration") or 0),
            thumbnail_url=info.get("thumbnail") or "",
        )
        return audio, raw

    async def _describe(self, track_id: str) -> tuple[str | None, str | None]:
        """Title and artist for a video whose audio we could not get: with them
        the track can still be found on another engine.

        Asked over oembed rather than the player: when youtube is refusing the
        download it refuses the player response too, while oembed keeps
        answering — and a name is all the fallback needs.
        """
        try:
            async with self.session.get(
                    "https://www.youtube.com/oembed",
                    params={"url": f"https://www.youtube.com/watch?v={track_id}", "format": "json"}
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    author = (data.get("author_name") or "").removesuffix(' - Topic')
                    return data.get("title"), author or None
        except Exception:  # noqa: BLE001 — a name is a bonus, not a requirement
            pass

        try:
            preview = await self.get_track(track_id)
            return preview.title, preview.artist_name
        except Exception:  # noqa: BLE001
            return None, None

    async def close(self):
        pass
