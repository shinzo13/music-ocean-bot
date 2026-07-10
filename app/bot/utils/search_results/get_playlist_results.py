import html

from aiogram_i18n.types import (
    InlineQueryResultArticle,
    InputTextMessageContent
)
from aiogram_i18n import LazyProxy

from app.bot.keyboards.entity_keyboard import entity_keyboard
from app.modules.musicocean.engines.shared.models import BasePlaylist
from app.modules.musicocean.enums.engine import Engine
from app.modules.musicocean_tg.utils import engine_to_prefix


async def get_playlist_results(
        engine: Engine,
        matches: list[BasePlaylist],
        bot_username: str
):
    return [
        InlineQueryResultArticle(
            id=f"{engine_to_prefix(engine)}_pl_{playlist.id}",
            title=playlist.title,
            description=f"{playlist.track_count} tracks",
            thumbnail_url=playlist.cover_url,
            input_message_content=InputTextMessageContent(
                message_text=LazyProxy(
                    'entity-playlist',
                    title=html.escape(playlist.title),
                    track_count=playlist.track_count,
                    cover_url=playlist.cover_url
                ),
                parse_mode='HTML'
            ),
            reply_markup=entity_keyboard(
                engine=engine,
                bot_username=bot_username,
                entity_id=playlist.id,
                prefix="pl"
            )

        )
        for playlist in matches
    ]
