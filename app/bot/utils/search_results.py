from app.database.repositories import TrackRepository
from app.modules.musicocean.enums import Engine
from app.modules.musicocean.models import TrackPreview
from aiogram.types import (
    InlineQueryResultAudio,
    InlineQueryResultCachedAudio,
    InlineQueryResultDocument,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResult
)

from app.config.log import get_logger

logger = get_logger(__name__)

engine_prefixes = {
    Engine.DEEZER       : "dz",
    Engine.SOUNDCLOUD   : "sc",
    Engine.YOUTUBE      : "yt",
    Engine.SPOTIFY      : "sp"
}


async def get_track_results(
    engine: Engine,
    matches: list[TrackPreview],
    track_repo: TrackRepository
): # TODO annotation

    reply_markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="downloading",
            callback_data="x"
        )
    ]])

    results = []
    for track in matches:
        db_track = await track_repo.get_track_by_id(track.id)
        logger.debug(f"(search) track '{track.title}': {db_track}")
        if db_track is not None:
            res = InlineQueryResultCachedAudio(
                id=f"cached_{engine_prefixes[engine]}_tr_{track.id}",
                audio_file_id=db_track.telegram_file_id
            )
        elif track.preview_url:
            res = InlineQueryResultAudio(
                id=f"{engine_prefixes[engine]}_tr_{track.id}",
                audio_url=track.preview_url,
                title=track.title,
                performer=track.artist_name, # not sure if needed
                reply_markup=reply_markup,
            )
        else:
            logger.debug(f"No preview_url for track #{track.id} ({engine})")
            res = InlineQueryResultDocument(
                id=f"{engine_prefixes[engine]}_tr_{track.id}",
                title=track.title,
                document_url=track.cover_url,
                mime_type="application/zip",
                reply_markup=reply_markup
            )
        results.append(res)

    return results