import html

from aiogram_i18n.types import (
    InlineQueryResultArticle,
    InputTextMessageContent
)
from aiogram_i18n import LazyProxy

from app.bot.keyboards.entity_keyboard import entity_keyboard
from app.modules.musicocean.engines.shared.models import BaseArtist
from app.modules.musicocean.enums.engine import Engine
from app.modules.musicocean_tg.utils import engine_to_prefix


async def get_artist_results(
        engine: Engine,
        matches: list[BaseArtist]
        , bot_username=None):
    return [
        InlineQueryResultArticle(
            id=f"{engine_to_prefix(engine)}_ar_{artist.id}",
            title=artist.name,
            description=f"{artist.listeners} listeners",
            thumbnail_url=artist.photo_url,
            input_message_content=InputTextMessageContent(
                message_text=LazyProxy(
                    'entity-artist',
                    name=artist.name,
                    listeners=artist.listeners,
                    cover_url=artist.cover_url
                ),
                parse_mode='HTML'
            ),
            reply_markup=entity_keyboard(
                engine=engine,
                bot_username=bot_username,
                entity_id=artist.id,
                prefix="ar",
                download_all=False
            )

        )
        for artist in matches
    ]
