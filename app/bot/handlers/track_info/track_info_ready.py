from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram_i18n import I18nContext
from dishka import FromDishka

from app.bot.keyboards import track_info_keyboard
from app.bot.utils.get_engine_emoji import get_engine_emoji
from app.config.log import get_logger
from app.database.models import User
from app.database.repositories import TrackRepository
from app.modules.musicocean.enums import Engine

logger = get_logger(__name__)

router = Router()


@router.message(F.audio)
async def track_info_ready(
        message: Message,
        bot: Bot,
        user: User,
        track_repo: FromDishka[TrackRepository],
        i18n: I18nContext
):
    track = await track_repo.get_track_by_file_id(message.audio.file_id)
    if not track:
        await message.answer(i18n.get('track-not-found'))
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
        bot_user = await bot.get_chat(track.user_id)
        downloaded_by = (
            '@' + bot_user.username if bot_user.username else
            f"<a href='tg://user?id={bot_user.id}'>{bot_user.first_name} {bot_user.last_name}</a>"
        ) if bot_user else f"<code>#{track.user_id}</code>"

        info += '\n' + i18n.get(
            'track-info-admin',
            track_id=str(track.track_id),  # fluent adds stupid spaces to int
            downloaded_by=downloaded_by
        )

    await message.answer(
        info,
        reply_markup=track_info_keyboard(track.track_id, track.engine)
    )
