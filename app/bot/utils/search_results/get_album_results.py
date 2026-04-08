from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent
)

from app.bot.keyboards.entity_keyboard import entity_keyboard
from app.bot.utils.get_engine_emoji import get_engine_emoji
from app.modules.musicocean.enums.engine import Engine
from app.modules.musicocean.models import Album
from app.modules.musicocean_tg.utils import engine_to_prefix


async def get_album_results(
        engine: Engine,
        matches: list[Album],
        bot_username: str
):
    emoji = get_engine_emoji(engine)
    return [
        InlineQueryResultArticle(
            id=f"{engine_to_prefix(engine)}_al_{album.id}",
            title=album.title,
            description=album.artist_name,
            thumbnail_url=album.cover_url,
            input_message_content=InputTextMessageContent(
                message_text=f'{emoji}<b>{album.title}</b>\n<i>{album.artist_name}</i><a href="{album.cover_url}">︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎</a>',
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
