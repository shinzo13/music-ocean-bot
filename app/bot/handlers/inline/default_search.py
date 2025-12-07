from aiogram import Router, F
from aiogram.types import InlineQuery
from dishka import FromDishka

from app.database.repositories import TrackRepository
from app.modules.musicocean_tg import TelegramMusicOceanClient
from app.modules.musicocean.enums.engine import Engine
from app.bot.utils.search_results import get_track_results
from app.config.log import get_logger
from app.database.models import User as DatabaseUser # TODO costyl

logger = get_logger(__name__)

router = Router()

@router.inline_query(F.query!="")
async def inline_query(
    query: InlineQuery,
    user: DatabaseUser,
    musicocean: FromDishka[TelegramMusicOceanClient],
    track_repo: FromDishka[TrackRepository]
):
    logger.info(f"User #{query.from_user.id} searched for \"{query.query}\"")
    # TODO inline engine selecting
    matches = await musicocean.search_tracks(user.selected_engine, query.query)
    await query.answer(await get_track_results(user.selected_engine, matches, track_repo))