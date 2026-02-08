from aiogram import Router, F
from aiogram.types import InlineQuery
from dishka import FromDishka

from app.bot.utils.search_results import get_track_results, usage_guide_result
from app.config.log import get_logger
from app.database.models import User
from app.modules.musicocean.exceptions import MusicOceanProviderDataException
from app.modules.musicocean_tg import TelegramMusicOceanClient
from app.modules.musicocean_tg.utils import prefix_to_engine

logger = get_logger(__name__)

router = Router()


@router.inline_query(F.query.regexp(r'^(dz|sc|yt|sp)::(al|ar|pl)::(\d+)$'))
async def inline_query(
        query: InlineQuery,
        musicocean: FromDishka[TelegramMusicOceanClient],
        user: User
):
    engine_prefix, entity_prefix, entity_id = query.query.split('::', maxsplit=2)
    logger.info(f"User #{query.from_user.id} searched for \"{query.query}\"")

    try:
        engine = prefix_to_engine(engine_prefix)
    except ValueError:
        await query.answer(usage_guide_result())
        return

    if not entity_id.isdigit():
        return  # TODO

    entity_id = int(entity_id)

    try:
        match entity_prefix:
            case 'al':
                matches = await musicocean.get_album_tracks(engine, entity_id)
            case 'ar':
                matches = await musicocean.get_artist_tracks(engine, entity_id)
            case 'pl':
                matches = await musicocean.get_playlist_tracks(engine, entity_id)
            case _:
                return  # TODO
    except MusicOceanProviderDataException:
        logger.debug("No data for that query")
        return

    logger.debug(f"matches: {matches}")

    await query.answer(
        await get_track_results(engine, matches, user.settings.track_preview_covers),
        cache_time=0,
        is_personal=True
    )
