from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent
)

from app.bot.constants import ENGINE_PREFIXES
from app.modules.musicocean.enums.engine import Engine
from app.modules.musicocean.models import Playlist


async def get_playlist_results(
        engine: Engine,
        matches: list[Playlist],
        bot_username: str
):
    return [
        InlineQueryResultArticle(
            id=f"{ENGINE_PREFIXES[engine]}_pl_{playlist.id}",
            title=playlist.title,
            description=f"{playlist.track_count} tracks",  # TODO maybe author instead
            thumbnail_url=playlist.cover_url,
            input_message_content=InputTextMessageContent(
                message_text=f'<b>{playlist.title}</b>\n<i>{playlist.track_count} tracks</i><a href="{playlist.cover_url}">︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎</a>',
            ),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="Search for track",
                    switch_inline_query_current_chat=f"{ENGINE_PREFIXES[engine]}::pl::{playlist.id}"
                )],
                [InlineKeyboardButton(
                    text="Download all tracks",
                    url=f"https://t.me/{bot_username}?start={ENGINE_PREFIXES[engine]}_pl_{playlist.id}"
                )]
            ])

        )
        for playlist in matches
    ]
