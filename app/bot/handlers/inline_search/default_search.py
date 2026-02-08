import re

from aiogram import Router, F
from aiogram.types import InlineQuery
from dishka import FromDishka

from app.bot.utils.search_results import get_track_results, usage_guide_result
from app.config.log import get_logger
from app.database.models import User as DatabaseUser  # TODO costyl
from app.modules.musicocean.enums.engine import Engine
from app.modules.musicocean_tg import TelegramMusicOceanClient
from app.modules.musicocean_tg.utils import prefix_to_engine

logger = get_logger(__name__)

router = Router()


@router.inline_query(F.query.regexp(r'^(?:(dz|sc|yt|sp):)?(.+)$').as_('match'))
async def inline_query(
        query: InlineQuery,
        match: re.Match,
        user: DatabaseUser,
        musicocean: FromDishka[TelegramMusicOceanClient],
):
    logger.info(f"User #{query.from_user.id} searched for \"{query.query}\"")

    engine_prefix, search_query = match.groups()

    try:
        engine = prefix_to_engine(engine_prefix)
    except ValueError:
        await query.answer(usage_guide_result())
        return

    logger.debug(f"Engine: {engine}, search query: \"{search_query}\"")
    matches = await musicocean.search_tracks(engine, search_query)
    await query.answer(
        await get_track_results(engine, matches, user.settings.track_preview_covers),
        cache_time=0,
        is_personal=True
    )
