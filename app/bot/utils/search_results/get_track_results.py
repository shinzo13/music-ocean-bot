import html

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton, InputTextMessageContent, InlineQueryResultArticle, InlineQueryResultAudio
)

from app.bot.constants import ENGINE_PREFIXES
from app.config.log import get_logger
from app.modules.musicocean.enums.engine import Engine
from app.modules.musicocean.models import TrackPreview

logger = get_logger(__name__)


async def get_track_results(
        engine: Engine,
        matches: list[TrackPreview],
        preview_covers: bool
):  # TODO annotation

    reply_markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="Downloading...",
            callback_data="x"
        )
    ]])

    results = []
    for track in matches:
        if preview_covers or not track.preview_url:
            res = InlineQueryResultArticle(
                id=f"{ENGINE_PREFIXES[engine]}_tr_{track.id}",
                title=track.title,
                description=track.artist_name,
                thumbnail_url=track.cover_url,
                input_message_content=InputTextMessageContent(
                    message_text=f"<i><b>🎧{html.escape(track.artist_name)} - {html.escape(track.title)}</b></i>"
                ),
                reply_markup=reply_markup
            )
        else:
            res = InlineQueryResultAudio(
                id=f"{ENGINE_PREFIXES[engine]}_tr_{track.id}",
                title=track.title,
                thumbnail_url=track.cover_url,
                audio_url=track.preview_url,
                performer=track.artist_name,
                input_message_content=InputTextMessageContent(
                    message_text=f"<i><b>🎧{html.escape(track.artist_name)} - {html.escape(track.title)}</b></i>"
                ),
                reply_markup=reply_markup
            )
        results.append(res)

    return results
