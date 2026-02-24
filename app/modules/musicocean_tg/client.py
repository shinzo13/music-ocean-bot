from typing import Optional, AsyncGenerator

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BufferedInputFile, URLInputFile, Message

from app.modules.musicocean.client import MusicOceanClient
from app.modules.musicocean.enums.engine import Engine
from app.modules.musicocean.models import TrackPreview
from app.modules.musicocean_tg.utils import engine_to_prefix
from app.modules.musicocean_tg.worker import TelegramWorker
from app.config import log

logger = log.get_logger(__name__)

# so fucking many abstractions
class TelegramMusicOceanClient(MusicOceanClient):
    def __init__(
            self,
            channel_id: int,
            bot_token: str,
            workers: Optional[list[str]],
            watermark: Optional[str]
    ):
        super().__init__(watermark)

        self.channel_id = channel_id
        self.main = TelegramWorker(
            token=bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self.workers = [
            TelegramWorker(
                token=worker_token,
                default=DefaultBotProperties(parse_mode=ParseMode.HTML)
            )
            for worker_token in workers
        ]


    async def checkup(self):
        for executor in self.workers+[self.main]:
            my_id = (await executor.get_me()).id
            try:
                await executor.get_chat(self.channel_id)
            except TelegramBadRequest:
                raise "please send some msg to channel and retry"
            adms = await executor.get_chat_administrators(self.channel_id)
            me = list(filter(lambda user: user.user.id == my_id, adms))[0]
            if not me.can_post_messages:
                raise "can't post messages"


    async def _download_track(
            self,
            engine: Engine,
            track_id: int,
            executor: TelegramWorker,
            force: bool = False,
    ) -> Message:
        logger.debug(f"downloading track {track_id}")
        track = await super().download_track(engine, track_id)
        logger.debug(f"success fetching")
        engine_prefix = engine_to_prefix(engine)
        sent_message = await executor.send_audio(
            self.channel_id,
            audio=BufferedInputFile(
                file=track.content,
                filename=f"{track.artist_name} – {track.title}.mp3"
            ),
            force=force,
            rate_timeout=60,
            title=track.title,
            thumbnail=URLInputFile(track.cover_url),
            performer=track.artist_name,
            duration=track.duration,
            caption=f"<code>{engine_prefix}-{track_id}</code>"
        )
        return sent_message

    async def download_track(self, engine: Engine, track_id: int) -> str:
        msg = await self._download_track(
            engine,
            track_id,
            self.main,
            force=True
        )
        return msg.audio.file_id

    def _get_available_worker(self) -> Optional[TelegramWorker]:
        for worker in self.workers:
            if worker.is_available():
                return worker
        return None


    async def download_tracks(
            self,
            engine: Engine,
            tracks: list[TrackPreview]
    ) -> AsyncGenerator[int, None]:
        tracks.reverse() # picking old first
        worker = self._get_available_worker()
        while tracks:
            if not worker.is_available():
                worker = None
                while not worker:
                    worker = self._get_available_worker()
            msg = await self._download_track(
                engine,
                (tracks.pop()).id,
                worker
            )
            yield msg.message_id