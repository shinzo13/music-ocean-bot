import asyncio
from typing import Optional, AsyncGenerator

from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BufferedInputFile, URLInputFile, Message

from app.config import log
from app.database.repositories import TrackRepository
from app.modules.musicocean.client import MusicOceanClient
from app.modules.musicocean.engines.shared.models import BaseTrackPreview
from app.modules.musicocean.enums.engine import Engine
from app.modules.musicocean_tg.models.cached_track import CachedTrack
from app.modules.musicocean_tg.utils import engine_to_prefix
from app.modules.musicocean_tg.worker import TelegramWorker

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

    async def _upload_track(
            self,
            engine: Engine,
            track_id: int | str,
            executor: TelegramWorker
    ) -> Message:
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
    async def download_track(
            self,
            engine: Engine,
            track_id: int | str
    ) -> CachedTrack:
        await self.main.wait_and_acquire(timeout=60)
        msg = await self._upload_track(engine, track_id, self.main)
        return CachedTrack(
            track_id=track_id,
            file_id=msg.audio.file_id,
            file_unique_id=msg.audio.file_unique_id
        )

    async def redownload_track(
            self,
            engine: Engine,
            track_id: int | str
    ) -> CachedTrack:
        # like download_track but routed through a worker, not the main bot
        worker = await self._acquire_worker()
        msg = await self._upload_track(engine, track_id, worker)
        return CachedTrack(
            track_id=track_id,
            file_id=msg.audio.file_id,
            file_unique_id=msg.audio.file_unique_id
        )

    async def _acquire_worker(self) -> TelegramWorker:
        while True:
            # least-loaded: пробуем наименее загруженных воркеров первыми,
            # чтобы нагрузка размазывалась ровно по всем, а не лилась в первого
            for worker in sorted(self.workers, key=lambda w: w.current_load()):
                if await worker.try_acquire():
                    return worker
            await asyncio.sleep(0.5)

    async def download_tracks(
            self,
            engine: Engine,
            tracks: list[BaseTrackPreview],
            track_repo: TrackRepository
    ) -> AsyncGenerator[CachedTrack, None]:

        cached = {
            t.id: await track_repo.get_track(t.id, engine)
            for t in tracks
        }

        # todo
        async def download_one(track_id: int | str) -> CachedTrack:
            if cached[track_id]:
                return CachedTrack(
                    track_id=track_id,
                    file_id=cached[track_id].telegram_file_id,  # noqa
                    file_unique_id=cached[track_id].telegram_file_unique_id  # noqa
                )
            worker = await self._acquire_worker()
            msg = await self._upload_track(engine, track_id, worker)

            return CachedTrack(
                track_id=track_id,
                file_id=msg.audio.file_id,
                file_unique_id=msg.audio.file_unique_id,
            )

        async def download_one_indexed(index: int, track_id: int | str):
            result = await download_one(track_id)
            return index, result

        futures = [download_one_indexed(i, t.id) for i, t in enumerate(tracks)]
        pending_results = {}
        next_yield = 0

        for coro in asyncio.as_completed(futures):
            idx, result = await coro
            pending_results[idx] = result
            while next_yield in pending_results:
                yield pending_results.pop(next_yield)
                next_yield += 1