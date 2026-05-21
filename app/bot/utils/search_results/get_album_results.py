import html

from aiogram_i18n.types import (
    InlineQueryResultArticle,
    InputTextMessageContent
)
from aiogram_i18n import LazyProxy

from app.bot.keyboards.entity_keyboard import entity_keyboard
from app.bot.utils.get_engine_emoji import get_engine_emoji
from app.modules.musicocean.engines.shared.models import BaseAlbum
from app.modules.musicocean.enums.engine import Engine
from app.modules.musicocean_tg.utils import engine_to_prefix


async def get_album_results(
        engine: Engine,
        matches: list[BaseAlbum],
        bot_username: str
):
    return [
        InlineQueryResultArticle(
            id=f"{engine_to_prefix(engine)}_al_{album.id}",
            title=album.title,
            description=album.artist_name,
            thumbnail_url=album.cover_url,
            input_message_content=InputTextMessageContent(
                message_text=LazyProxy(
                    'entity-album',
                    title=album.title,
                    artist_name=album.artist_name,
                    cover_url=album.cover_url
                ),
                parse_mode='HTML'
            ),
            reply_markup=entity_keyboard(
                engine=engine,
                bot_username=bot_username,
                entity_id=album.id,
                prefix="al"
            )

        )
        for album in matches
    ]
