from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BufferedInputFile, URLInputFile
from aiogram.enums.parse_mode import ParseMode

from app.modules.musicocean.client import MusicOceanClient
from aiogram import Bot

from app.modules.musicocean.enums.engine import Engine


# so fucking many abstractions
class TelegramMusicOceanClient(MusicOceanClient):
    def __init__(self, channel_id: int, bot_token: str):
        super().__init__()

        # нуу дубликат но вроде же похуй да
        self.bot = Bot(
            token=bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self.channel_id = channel_id

    async def checkup(self):
        my_id = (await self.bot.get_me()).id
        try:
            await self.bot.get_chat(self.channel_id)
        except TelegramBadRequest:
            raise "please send some msg to channel and retry"
        adms = await self.bot.get_chat_administrators(self.channel_id)
        me = list(filter(lambda user: user.user.id == my_id, adms))[0]
        if not me.can_post_messages:
            raise "can't post messages"
        # similar checkup for workers here

    async def download_track(self, engine: Engine, track_id: int) -> str:
        track = await super().download_track(engine, track_id)
        file_id = (await self.bot.send_audio(
            self.channel_id,
            audio=BufferedInputFile(
                file=track.content,
                filename=f"{track.artist_name} – {track.title}.mp3"
            ),
            title=track.title,
            thumbnail=URLInputFile(track.cover_url),
            performer=track.artist_name,
            duration=track.duration,
            caption=f"<code>{track_id}</code>"
        )).audio.file_id
        return file_id



