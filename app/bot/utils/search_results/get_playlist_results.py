import html

from aiogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent
)

from app.bot.keyboards.entity_keyboard import entity_keyboard
from app.modules.musicocean.enums.engine import Engine
from app.modules.musicocean.engines.shared.models import BasePlaylist
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
            description=f"{playlist.track_count} tracks",  # TODO maybe author instead
            thumbnail_url=playlist.cover_url,
            input_message_content=InputTextMessageContent(
                message_text=f'<b>{html.escape(playlist.title)}</b>\n<i>{playlist.track_count} tracks</i><a href="{playlist.cover_url}">︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎</a>',
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
