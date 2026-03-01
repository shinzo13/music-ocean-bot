from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent
)

from app.bot.keyboards.entity_keyboard import entity_keyboard
from app.modules.musicocean.enums.engine import Engine
from app.modules.musicocean.models import Artist
from app.modules.musicocean_tg.utils import engine_to_prefix


async def get_artist_results(
        engine: Engine,
        matches: list[Artist]
, bot_username=None):
    return [
        InlineQueryResultArticle(
            id=f"{engine_to_prefix(engine)}_ar_{artist.id}",
            title=artist.name,
            description=f"{artist.listeners} listeners",
            thumbnail_url=artist.photo_url,
            input_message_content=InputTextMessageContent(
                message_text=f'<b>{artist.name}</b>\n<i>{artist.listeners} listeners</i><a href="{artist.photo_url}">︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎</a>',
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
