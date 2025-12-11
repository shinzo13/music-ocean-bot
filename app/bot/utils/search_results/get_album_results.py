from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent
)

from app.bot.constants import ENGINE_PREFIXES
from app.modules.musicocean.enums.engine import Engine
from app.modules.musicocean.models import Album


async def get_album_results(
        engine: Engine,
        matches: list[Album],
        bot_username: str
):
    return [
        InlineQueryResultArticle(
            id=f"{ENGINE_PREFIXES[engine]}_al_{album.id}",
            title=album.title,
            description=album.artist_name,
            thumbnail_url=album.cover_url,
            input_message_content=InputTextMessageContent(
                message_text=f'<b>{album.title}</b>\n<i>{album.artist_name}</i><a href="{album.cover_url}">︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎</a>',
            ),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="Search for track",
                    switch_inline_query_current_chat=f"{ENGINE_PREFIXES[engine]}::al::{album.id}"
                )],
                [InlineKeyboardButton(
                    text="Download all tracks",
                    url=f"https://t.me/{bot_username}?start={ENGINE_PREFIXES[engine]}_al_{album.id}"
                )]
            ])

        )
        for album in matches
    ]
