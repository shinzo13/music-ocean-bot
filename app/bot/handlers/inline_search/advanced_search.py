import re

from aiogram import Router, F, Bot
from aiogram.types import InlineQuery
from dishka import FromDishka

from app.bot.utils.search_results import (
    get_album_results,
    get_artist_results,
    get_playlist_results,
    usage_guide_result
)
from app.config.log import get_logger
from app.database.models import User as DatabaseUser
from app.modules.musicocean.enums.engine import Engine
from app.modules.musicocean_tg import TelegramMusicOceanClient
from app.modules.musicocean_tg.utils import prefix_to_engine

logger = get_logger(__name__)

router = Router()

REGEX = r'^(?:(dz|sc|yt|sp):)?(al|album|pl|playlist|ar|artist):(.+)$'


@router.inline_query(F.query.regexp(REGEX).as_('match'))
async def inline_query(
        query: InlineQuery,
        match: re.Match,
        bot: Bot,
        user: DatabaseUser,
        musicocean: FromDishka[TelegramMusicOceanClient]
):
    logger.info(f"User #{query.from_user.id} searched for \"{query.query}\"")
    engine_prefix, entity_prefix, search_query = match.groups()

    if not engine_prefix:
        engine = user.settings.selected_engine
    else:
        try:
            engine = prefix_to_engine(engine_prefix)
        except ValueError:
            await query.answer(usage_guide_result())
            return

    bot_username = (await bot.get_me()).username

    match entity_prefix:
        case "al" | "album":
            matches = await musicocean.search_albums(engine, search_query)
            results = await get_album_results(engine, matches, bot_username)
        case "ar" | "artist":
            matches = await musicocean.search_artists(engine, search_query)
            results = await get_artist_results(engine, matches)
        case "pl" | "playlist":
            matches = await musicocean.search_playlists(engine, search_query)
            results = await get_playlist_results(engine, matches, bot_username)
        case "" | _:
            results = usage_guide_result()

    await query.answer(results)
