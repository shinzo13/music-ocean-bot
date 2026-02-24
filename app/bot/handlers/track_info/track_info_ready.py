from aiogram import Bot, Router, F
from aiogram.types import Message
from dishka import FromDishka

from app.bot.keyboards import track_info_keyboard
from app.database.models import User
from app.database.repositories import TrackRepository
from app.modules.musicocean.enums import Engine

router = Router()

@router.message(F.audio)
async def track_info_ready(
        message: Message,
        bot: Bot,
        user: User,
        track_repo: FromDishka[TrackRepository]
):
    track = await track_repo.get_track_by_file_id(message.audio.file_id)
    if not track:
        await message.answer("track is not from music ocean bla bla bla")
        # todo watermark checking here after prompting user
        return

    engine_names = {
        Engine.DEEZER: "Deezer",
        Engine.SOUNDCLOUD: "SoundCloud",
        Engine.YOUTUBE: "YouTube",
        Engine.SPOTIFY: "Spotify"
    }

    info = (
        f"{message.audio.performer} - {message.audio.title}\n"
        f"Downloaded from {engine_names[track.engine]}"
    )

    if user.is_admin:
        track_user = await bot.get_chat(track.user_id)
        downloaded_by = (
            '@'+track_user.username or
            f"{track_user.first_name} {track_user.last_name}"
        ) if track_user else f"#{track.user_id}"
        info += (
            f"\n\nTrack ID: {track.track_id}\n"
            f"Downloaded by: {downloaded_by}"
        )

    await message.answer(
        info,
        reply_markup=track_info_keyboard(track.track_id, track.engine)
    )