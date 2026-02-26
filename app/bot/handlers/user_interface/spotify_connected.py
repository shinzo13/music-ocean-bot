from aiogram import Router, F
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message
import re

from dishka import FromDishka

from app.bot.utils.get_engine_emoji import get_engine_emoji
from app.config import settings
from app.database.models import User
from app.database.repositories import UserRepository
from app.modules.musicocean_tg import TelegramMusicOceanClient
from app.modules.musicocean_tg.utils import prefix_to_engine

router = Router()


@router.message(
    CommandStart(
        deep_link=True,
        magic=F.args=="spotify_connect"
    )
)
async def spotify_connected(
        message: Message,
        user: User,
        musicocean: FromDishka[TelegramMusicOceanClient],
        user_repo: FromDishka[UserRepository]
):
    await message.delete()
    if user.settings.spotify.enabled:
        await message.answer("already connected tf are you doing")
        return
    if not user.settings.spotify.connection_code:
        await message.answer("smth went wrong")
        return

    access_token, refresh_token = await musicocean.exchange_spotify_code(
        user.settings.spotify.connection_code,
        f"https://{settings.server.domain}/spotify"
    )

    await user_repo.update_user_settings(
        user_id=user.id,
        spotify__enabled=True,
        spotify__access_token=access_token,
        spotify__refresh_token=refresh_token
    )

    await message.answer("ok")
