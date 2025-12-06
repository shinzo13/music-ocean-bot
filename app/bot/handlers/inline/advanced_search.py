import re

from aiogram import Router, F, Bot
from aiogram.types import InlineQuery
from dishka import FromDishka

from app.bot.constants import ENTITY_PREFIXES
from app.database.repositories import TrackRepository
from app.modules.musicocean.enums import EntityType
from app.modules.musicocean_tg import TelegramMusicOceanClient
from app.modules.musicocean.enums.engine import Engine
from app.bot.utils.search_results import (
    get_track_results,
    get_album_results,
    get_artist_results,
    get_playlist_results,
    usage_guide_result
)
from app.config.log import get_logger
from app.database.models import User as DatabaseUser


logger = get_logger(__name__)

router = Router()


@router.inline_query(F.query.regexp(r'^(al|album|ar|artist|pl|playlist):(.+)$'))
async def inline_query(
        query: InlineQuery,
        bot: Bot,
        user: DatabaseUser,
        musicocean: FromDishka[TelegramMusicOceanClient]
):
    logger.info(f"User #{query.from_user.id} searched for \"{query.query}\"")
    entity_prefix, search_query = query.query.split(':', maxsplit=1)
    bot_username = (await bot.get_me()).username
    # TODO inline engine selecting
    match entity_prefix:
        case "al" | "album":
            matches = await musicocean.search_albums(user.selected_engine, search_query)
            results = await get_album_results(user.selected_engine, matches, bot_username)
        case "ar" | "artist":
            matches = await musicocean.search_artists(user.selected_engine, search_query)
            results = await get_artist_results(user.selected_engine, matches)
        case "pl" | "playlist":
            matches = await musicocean.search_playlists(user.selected_engine, search_query)
            results = await get_playlist_results(user.selected_engine, matches, bot_username)
        case "" | _:
            results = usage_guide_result()

    await query.answer(results)
