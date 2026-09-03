"""Audio straight off youtube's /player endpoint.

Youtube hands most of its clients stream urls whose signature has to be
deciphered by running the player javascript — that is what the download
libraries spend their weight on, and what breaks whenever the player changes.
A couple of clients are still answered with plain urls, so this module asks as
one of those and needs nothing but http.

The transfer is taken in ranges on purpose: a single open-ended GET is shaped
down to a trickle (~30 KB/s), while the same file fetched as ranges arrives at
full speed.
"""
import asyncio
import io
from dataclasses import dataclass
from typing import Awaitable, Callable

from aiohttp import ClientSession

from app.config.log import get_logger
from app.modules.musicocean.engines.youtube.constants import (
    PLAYER_CLIENTS, YT_BASE_API,
)
from app.modules.musicocean.engines.youtube.exceptions import (
    YoutubeDataException, YoutubeRefusedException, YoutubeUnavailableException,
)

logger = get_logger(__name__)

CHUNK_SIZE = 1 << 20
CHUNK_CONCURRENCY = 4


@dataclass
class PlayerInfo:
    """What one /player answer tells us about a video."""

    id: str
    title: str
    author: str
    duration: int
    thumbnail_url: str
    itag: int
    audio_url: str
    audio_size: int
    # the url is issued to the client that asked for it — the transfer keeps
    # the same user agent
    user_agent: str


class InnertubePlayer:
    def __init__(
            self,
            session: ClientSession,
            visitor_id: Callable[[bool], Awaitable[str]],
    ):
        self.session = session
        self._visitor_id = visitor_id

    async def info(self, video_id: str) -> PlayerInfo:
        """Metadata and a usable audio url, trying each client in turn.

        A second pass runs with a freshly fetched visitor id: a refusal is
        normally tied to the identity we asked with, not to the video.
        """
        last: Exception | None = None

        for attempt in range(2):
            visitor = await self._visitor_id(attempt > 0)
            for client in PLAYER_CLIENTS:
                try:
                    data = await self._player(video_id, client, visitor)
                    return self._parse(video_id, data, client)
                except YoutubeUnavailableException:
                    # every client gets the same answer for a video that is
                    # really gone, so there is nothing left to try
                    raise
                except Exception as e:  # noqa: BLE001 — try the next client
                    last = e
                    logger.debug(
                        f"yt: {client['name']} refused {video_id}: "
                        f"{type(e).__name__} {e}"
                    )

        raise YoutubeRefusedException(f"no client served {video_id}: {last!r}")

    async def download(self, info: PlayerInfo) -> bytes:
        """The audio itself, pulled in parallel ranges."""
        slots = asyncio.Semaphore(CHUNK_CONCURRENCY)

        async def part(start: int) -> tuple[int, bytes]:
            end = min(start + CHUNK_SIZE - 1, info.audio_size - 1)
            async with slots:
                async with self.session.get(
                        f"{info.audio_url}&range={start}-{end}",
                        headers={"User-Agent": info.user_agent},
                ) as resp:
                    if resp.status != 200:
                        raise YoutubeRefusedException(
                            f"stream answered http {resp.status}"
                        )
                    return start, await resp.read()

        starts = range(0, info.audio_size, CHUNK_SIZE)
        parts = await asyncio.gather(*[part(s) for s in starts])

        buffer = io.BytesIO()
        for _, chunk in sorted(parts):
            buffer.write(chunk)
        raw = buffer.getvalue()

        # youtube tells us the exact size up front, so a mismatch means the
        # transfer was cut and the file would be silently truncated
        if len(raw) != info.audio_size:
            raise YoutubeRefusedException(
                f"short read: {len(raw)} of {info.audio_size} bytes"
            )
        return raw

    async def _player(self, video_id: str, client: dict, visitor: str) -> dict:
        body = {
            "context": {
                "client": {
                    **client["context"],
                    "hl": "en",
                    "gl": "US",
                    "visitorData": visitor,
                }
            },
            "videoId": video_id,
            "contentCheckOk": True,
            "racyCheckOk": True,
        }
        headers = {
            "User-Agent": client["ua"],
            "X-Goog-Visitor-Id": visitor,
            "X-Youtube-Client-Name": str(client["id"]),
            "X-Youtube-Client-Version": client["context"]["clientVersion"],
            "Content-Type": "application/json",
        }
        async with self.session.post(
                f"{YT_BASE_API}/player", json=body, headers=headers
        ) as resp:
            if resp.status != 200:
                raise YoutubeRefusedException(f"player answered http {resp.status}")
            return await resp.json()

    @staticmethod
    def _parse(video_id: str, data: dict, client: dict) -> PlayerInfo:
        status = data.get("playabilityStatus", {})
        state = status.get("status")
        if state != "OK":
            reason = status.get("reason") or state
            # "sign in to confirm you're not a bot" is aimed at us and another
            # client may well be let through; anything else is about the video
            if state == "LOGIN_REQUIRED" and "bot" in str(reason).lower():
                raise YoutubeRefusedException(f"{video_id}: {reason}")
            raise YoutubeUnavailableException(f"{video_id}: {reason}")

        formats = data.get("streamingData", {}).get("adaptiveFormats", [])
        audio = [
            f for f in formats
            if f.get("mimeType", "").startswith("audio/mp4")
            and f.get("url") and f.get("contentLength")
        ]
        if not audio:
            raise YoutubeRefusedException(f"{video_id}: no plain audio format offered")
        best = max(audio, key=lambda f: f.get("bitrate", 0))

        details = data.get("videoDetails", {})
        thumbnails = details.get("thumbnail", {}).get("thumbnails", [])
        if not details.get("title"):
            raise YoutubeDataException(f"{video_id}: player answer has no title")

        return PlayerInfo(
            id=video_id,
            title=details["title"],
            author=(details.get("author") or "?").removesuffix(" - Topic"),
            duration=int(details.get("lengthSeconds") or 0),
            thumbnail_url=thumbnails[-1]["url"] if thumbnails else "",
            itag=best["itag"],
            audio_url=best["url"],
            audio_size=int(best["contentLength"]),
            user_agent=client["ua"],
        )
