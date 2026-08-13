import html

from aiogram_i18n.types import (
    InputTextMessageContent, InlineQueryResultArticle, InlineQueryResultAudio
)

from app.bot.keyboards.download_button import download_keyboard
from app.config.log import get_logger
from app.modules.musicocean.engines.shared.models import BaseTrackPreview
from app.modules.musicocean.enums.engine import Engine
from app.modules.musicocean_tg.utils import engine_to_prefix

logger = get_logger(__name__)


async def get_track_results(
        engine: Engine,
        matches: list[BaseTrackPreview],
        preview_covers: bool,
        ctx: str = "s"
):  # TODO annotation

    # engines happily return the same track twice (re-releases, mixed sources);
    # telegram rejects the whole answer with RESULT_ID_DUPLICATE if ids repeat
    unique: list[BaseTrackPreview] = []
    seen: set[int | str] = set()
    for track in matches:
        if track.id in seen:
            continue
        seen.add(track.id)
        unique.append(track)
    if len(unique) != len(matches):
        logger.debug(f"dropped {len(matches) - len(unique)} duplicate track ids")

    results = []
    # telegram allows at most 50 inline results per answer
    for track in unique[:50]:
        text = f"<i><b>♫ {html.escape(track.artist_name)}</b> - {html.escape(track.title)}</i>"
        track_ref = f"{engine_to_prefix(engine)}_tr_{ctx}_{track.id}"
        reply_markup = download_keyboard(track_ref)
        if preview_covers or not track.preview_url:
            res = InlineQueryResultArticle(
                id=track_ref,
                title=track.title,
                description=track.artist_name,
                thumbnail_url=track.cover_url,
                input_message_content=InputTextMessageContent(
                    message_text=text,
                    parse_mode='HTML'
                ),
                reply_markup=reply_markup
            )
        else:
            res = InlineQueryResultAudio(
                id=track_ref,
                title=track.title,
                thumbnail_url=track.cover_url,
                audio_url=track.preview_url,
                performer=track.artist_name,
                input_message_content=InputTextMessageContent(
                    message_text=text,
                    parse_mode='HTML'
                ),
                reply_markup=reply_markup
            )
        results.append(res)

    return results
