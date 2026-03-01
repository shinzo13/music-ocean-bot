from aiogram import Router, F, Bot
from aiogram.types import InlineQuery
from dishka import FromDishka

from app.bot.utils.search_results import setup_scrobbling_result, get_track_results
from app.config.log import get_logger
from app.database.models import User as DatabaseUser  # TODO costyl
from app.modules.musicocean.enums import Engine
from app.modules.musicocean_tg import TelegramMusicOceanClient

logger = get_logger(__name__)

router = Router()


@router.inline_query(F.query == "")
async def inline_query(
        query: InlineQuery,
        bot: Bot,
        user: DatabaseUser,
        musicocean: FromDishka[TelegramMusicOceanClient],
):
    logger.info(f"User #{query.from_user.id}: empty search query")
    if not user.settings.spotify.enabled:
        await query.answer(setup_scrobbling_result(
            (await bot.get_me()).username
        ))

    # todo saving updated refresh_token
    # but probably in other way..
    track, _ = await musicocean.get_spotify_last_track(
        user.settings.spotify.access_token,
        user.settings.spotify.refresh_token
    )

    if not track:
        return

    await query.answer(
        await get_track_results(
            Engine.SPOTIFY,
            [track],
            user.settings.track_preview_covers
        ),
        cache_time=0
    )