import html

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton, InputTextMessageContent, InlineQueryResultArticle, InlineQueryResultAudio
)

from app.config.log import get_logger
from app.modules.musicocean.enums.engine import Engine
from app.modules.musicocean.models import TrackPreview
from app.modules.musicocean_tg.utils import engine_to_prefix

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
        text = f"<i><b>♫ {html.escape(track.artist_name)}</b> - {html.escape(track.title)}</i>"
        if preview_covers or not track.preview_url:
            res = InlineQueryResultArticle(
                id=f"{engine_to_prefix(engine)}_tr_{track.id}",
                title=track.title,
                description=track.artist_name,
                thumbnail_url=track.cover_url,
                input_message_content=InputTextMessageContent(
                    message_text=text
                ),
                reply_markup=reply_markup
            )
        else:
            res = InlineQueryResultAudio(
                id=f"{engine_to_prefix(engine)}_tr_{track.id}",
                title=track.title,
                thumbnail_url=track.cover_url,
                audio_url=track.preview_url,
                performer=track.artist_name,
                input_message_content=InputTextMessageContent(
                    message_text=text
                ),
                reply_markup=reply_markup
            )
        results.append(res)

    return results
