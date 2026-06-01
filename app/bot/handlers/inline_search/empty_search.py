from aiogram import Router, F, Bot
from aiogram.types import InlineQuery
from dishka import FromDishka

from app.bot.utils.search_results import setup_scrobbling_result, get_track_results
from app.config.log import get_logger
from app.database.models import User as DatabaseUser  # TODO costyl
from app.modules.musicocean.enums import Engine
from app.modules.musicocean.lastfm.exceptions import LastFMNoDataException, LastFMNoProvidersException
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
    if not user.settings.lastfm.enabled:
        await query.answer(
            setup_scrobbling_result((await bot.get_me()).username),
            cache_time=0,
            is_personal=True
        )
        return

    try:
        track_data = await musicocean.lastfm.get_recent_track_data(
            username=user.settings.lastfm.username
        )
    except LastFMNoDataException:
        # todo "your scrobbling is kinda broken ngl"
        return

    try:
        engine, track = await musicocean.lastfm.get_provider_track(
            track_data=track_data
        )
    except LastFMNoProvidersException:
        logger.info(f"Falling back to YT matching while getting scrobbled track {track_data.title}")
        track = await musicocean.youtube.search_exact_match(
            track_data.title,
            track_data.artist_name
        )
        if not track:
            logger.info(f"Cant get scrobbled track {track_data.title}")
            return
        engine = Engine.YOUTUBE

    await query.answer(
        await get_track_results(
            engine,
            [track],
            user.settings.track_preview_covers
        ),
        cache_time=0,
        is_personal=True
    )
