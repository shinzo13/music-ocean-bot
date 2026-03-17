from aiogram import Router, F
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message
import re

from dishka import FromDishka

from app.bot.keyboards.scrobbling import oauth_scrobbling_keyboard
from app.bot.utils.get_engine_emoji import get_engine_emoji
from app.config import settings
from app.config.log import get_logger
from app.database.models import User
from app.database.repositories import UserRepository
from app.modules.musicocean_tg import TelegramMusicOceanClient
from app.modules.musicocean_tg.utils import prefix_to_engine


logger = get_logger(__name__)
router = Router()


@router.message(
    CommandStart(
        deep_link=True,
        magic=F.args=="setup_scrobbling"
    )
)
async def setup_scrobbling_handler(
        message: Message,
        user: User
):
    await message.delete()
    if user.settings.spotify.enabled:
        await message.answer("already connected tf are you doing")
        return
    await message.answer(
        "login",
        reply_markup=oauth_scrobbling_keyboard(user.user_id)
    )

@router.message(
    CommandStart(
        deep_link=True,
        magic=F.args=="spotify_connected"
    )
)
async def spotify_connected_handler(
        message: Message,
        user: User,
        musicocean: FromDishka[TelegramMusicOceanClient],
        user_repo: FromDishka[UserRepository]
):
    ...
# TODO