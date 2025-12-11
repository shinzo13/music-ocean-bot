import html

from app.database.repositories import TrackRepository
from app.modules.musicocean.enums.engine import Engine
from app.modules.musicocean.models import TrackPreview, Album, Artist, Playlist
from aiogram.types import (
    InlineQueryResultAudio,
    InlineQueryResultCachedAudio,
    InlineQueryResultDocument,
    InlineKeyboardMarkup,
    InlineKeyboardButton, InputTextMessageContent, InlineQueryResultArticle
)

from app.config.log import get_logger
from app.bot.constants import ENGINE_PREFIXES

logger = get_logger(__name__)

async def get_track_results(
    engine: Engine,
    matches: list[TrackPreview]
): # TODO annotation

    reply_markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="Downloading...",
            callback_data="x"
        )
    ]])

    results = []
    for track in matches:
        # TODO implement user settings and add sending-preview option here
        logger.debug(f"{track.title=} {track.artist_name=}")
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
        results.append(res)

    return results
