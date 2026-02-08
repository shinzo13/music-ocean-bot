from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent
)

from app.modules.musicocean.enums.engine import Engine
from app.modules.musicocean.models import Artist
from app.modules.musicocean_tg.utils import engine_to_prefix


async def get_artist_results(
        engine: Engine,
        matches: list[Artist]
):
    return [
        InlineQueryResultArticle(
            id=f"{engine_to_prefix(engine)}_ar_{artist.id}",
            title=artist.name,
            description=f"{artist.listeners} listeners",
            thumbnail_url=artist.photo_url,
            input_message_content=InputTextMessageContent(
                message_text=f'<b>{artist.name}</b>\n<i>{artist.listeners} listeners</i><a href="{artist.photo_url}">︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎</a>',
            ),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="Search for track",
                    switch_inline_query_current_chat=f"{engine_to_prefix(engine)}::ar::{artist.id}"
                )]
            ])

        )
        for artist in matches
    ]
