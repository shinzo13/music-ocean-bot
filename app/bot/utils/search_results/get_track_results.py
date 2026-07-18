import html

from aiogram_i18n.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton, InputTextMessageContent, InlineQueryResultArticle, InlineQueryResultAudio
)
from aiogram_i18n import LazyProxy

from app.bot.constants import LOADING_EMOJI_ID
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

    reply_markup = InlineKeyboardMarkup(inline_keyboard=[[ # noqa
        InlineKeyboardButton(
            text=LazyProxy('btn-downloading'),
            callback_data="meow mrrnyaahhhhh",
            icon_custom_emoji_id=LOADING_EMOJI_ID
        )
    ]])

    results = []
    # telegram allows at most 50 inline results per answer
    for track in matches[:50]:
        text = f"<i><b>♫ {html.escape(track.artist_name)}</b> - {html.escape(track.title)}</i>"
        if preview_covers or not track.preview_url:
            res = InlineQueryResultArticle(
                id=f"{engine_to_prefix(engine)}_tr_{ctx}_{track.id}",
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
                id=f"{engine_to_prefix(engine)}_tr_{ctx}_{track.id}",
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
