from aiogram import Router, F
from aiogram.types import Message
from dishka import FromDishka

from app.config import settings
from app.config.log import get_logger
from app.modules.musicocean_tg import TelegramMusicOceanClient

logger = get_logger(__name__)

router = Router()


@router.channel_post(F.audio and F.chat.id == settings.telegram.channel_id)
async def on_pending_track(
        message: Message,
        musicocean: FromDishka[TelegramMusicOceanClient]
):
    if message.message_id in musicocean.pending:
        future = musicocean.pending.pop(message.message_id)
        future.set_result(message.audio.file_id)
        logger.debug(f"Caught pending track with message_id={message.message_id}")