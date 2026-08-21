from aiogram import Bot, Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from aiogram_i18n import I18nContext
from dishka import FromDishka

from app.bot.keyboards import track_info_keyboard
from app.bot.utils.get_engine_emoji import get_engine_emoji
from app.config import settings
from app.config.log import get_logger
from app.database.models import User
from app.database.repositories import TrackRepository, UserRepository
from app.modules.musicocean.enums import Engine

logger = get_logger(__name__)

router = Router()


def _link(user_id: int, first_name: str | None, last_name: str | None, username: str | None) -> str:
    if username:
        return '@' + username
    name = " ".join(p for p in (first_name, last_name) if p)
    return f"<a href='tg://user?id={user_id}'>{name}</a>" if name else f"<code>#{user_id}</code>"


async def describe_downloader(bot: Bot, user_repo: UserRepository, user_id: int) -> str:
    """Who downloaded a track, for the admin line.

    Our own users table first: it already holds the name and handle, kept fresh
    on every message. get_chat is only a fallback, and a failing one — a
    downloader who never opened a private chat with the bot, or who came in as
    an anonymous channel, answers "chat not found" and used to take the whole
    reply down with it.
    """
    known = await user_repo.get_user_by_id(user_id)
    if known:
        return _link(user_id, known.first_name, known.last_name, known.username)

    try:
        chat = await bot.get_chat(user_id)
    except TelegramBadRequest:
        return f"<code>#{user_id}</code>"
    return _link(user_id, chat.first_name, chat.last_name, chat.username)


@router.message(F.audio)
async def track_info_ready(
        message: Message,
        bot: Bot,
        user: User,
        track_repo: FromDishka[TrackRepository],
        user_repo: FromDishka[UserRepository],
        i18n: I18nContext
):
    track = await track_repo.get_track_by_file(
        message.audio.file_unique_id,
        message.audio.file_id
    )
    if not track:
        await message.answer(i18n.get('track-not-found', brand=settings.local.brand))
        # todo watermark checking here after prompting user
        return

    engine_names = {
        Engine.DEEZER: "Deezer",
        Engine.SOUNDCLOUD: "SoundCloud",
        Engine.YOUTUBE: "YouTube",
        Engine.SPOTIFY: "Spotify",
        Engine.YANDEX: "Yandex Music"
    }

    info = i18n.get(
        'track-info',
        artist_name=message.audio.performer,
        title=message.audio.title,
        engine_emoji=get_engine_emoji(track.engine),
        engine_name=engine_names[track.engine]
    )

    if user.is_admin:
        downloaded_by = await describe_downloader(bot, user_repo, track.user_id)

        info += '\n' + i18n.get(
            'track-info-admin',
            track_id=str(track.track_id),  # fluent adds stupid spaces to int
            downloaded_by=downloaded_by
        )

    await message.answer(
        info,
        reply_markup=track_info_keyboard(track.track_id, track.engine)
    )
