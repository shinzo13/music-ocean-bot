import asyncio
from typing import Optional, AsyncGenerator

from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BufferedInputFile, URLInputFile, Message

from app.database.repositories import TrackRepository
from app.modules.musicocean.client import MusicOceanClient
from app.modules.musicocean.enums.engine import Engine
from app.modules.musicocean.models import TrackPreview
from app.modules.musicocean_tg.models.cached_track import CachedTrack
from app.modules.musicocean_tg.utils import engine_to_prefix
from app.modules.musicocean_tg.worker import TelegramWorker
from app.config import log

logger = log.get_logger(__name__)


class TelegramMusicOceanClient(MusicOceanClient):
    pending: dict[int, asyncio.Future[str]] = {}

    def __init__(self, channel_id: int, bot_token: str, workers: Optional[list[str]], watermark: Optional[str]):
        super().__init__(watermark)
        self.channel_id = channel_id
        self.main = TelegramWorker(
            token=bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self.workers = [
            TelegramWorker(token=t, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
            for t in workers
        ]
        self.pending = {}

    async def checkup(self):
        for executor in self.workers + [self.main]:
            my_id = (await executor.get_me()).id
            try:
                await executor.get_chat(self.channel_id)
            except TelegramBadRequest:
                raise "please send some msg to channel and retry"
            adms = await executor.get_chat_administrators(self.channel_id)
            me = next(u for u in adms if u.user.id == my_id)
            if not me.can_post_messages:
                raise "can't post messages"

    async def _upload_track(self, engine: Engine, track_id: int, executor: TelegramWorker) -> Message:
        logger.debug(f"downloading track {track_id}")
        track = await super().download_track(engine, track_id)
        engine_prefix = engine_to_prefix(engine)
        logger.debug(f"uploading track {track_id}")
        return await executor.send_audio(
            self.channel_id,
            audio=BufferedInputFile(file=track.content, filename=f"{track.artist_name} – {track.title}.mp3"),
            title=track.title,
            thumbnail=URLInputFile(track.cover_url),
            performer=track.artist_name,
            duration=track.duration,
            caption=f"<code>{engine_prefix}-{track_id}</code>"
        )

    # todo another naming
    async def download_track(self, engine: Engine, track_id: int) -> CachedTrack:
        await self.main.wait_and_acquire(timeout=60)
        msg = await self._upload_track(engine, track_id, self.main)
        return CachedTrack(
            track_id=track_id,
            file_id=msg.audio.file_id
        )

    async def _acquire_worker(self) -> TelegramWorker:
        while True:
            for worker in self.workers:
                if await worker.try_acquire():
                    return worker
            await asyncio.sleep(0.5)

    async def download_tracks(
            self,
            engine: Engine,
            tracks: list[TrackPreview],
            track_repo: TrackRepository
    ) -> AsyncGenerator[CachedTrack, None]:
        #tracks.reverse()

        cached = {
            t.id: await track_repo.get_track(t.id, engine)
            for t in tracks
        }

        async def download_one(track_id: int) -> CachedTrack:
            if cached[track_id]:
                return CachedTrack(
                    track_id=track_id,
                    file_id=cached[track_id].telegram_file_id # noqa
                )
            worker = await self._acquire_worker()
            msg = await self._upload_track(engine, track_id, worker)
            future = asyncio.get_event_loop().create_future()
            self.pending[msg.message_id] = future
            logger.debug(f"pending track with message_id={msg.message_id}...")
            file_id = await future
            return CachedTrack(
                track_id=track_id,
                file_id=file_id
            )

        futures = [asyncio.ensure_future(download_one(t.id)) for t in tracks]
        for future in futures:
            yield await future