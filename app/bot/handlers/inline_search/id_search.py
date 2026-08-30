from aiogram import Router, F
from aiogram.types import InlineQuery
from aiogram_i18n import I18nContext
from dishka import FromDishka

from app.bot.utils.search_results import get_track_results, not_supported_result, usage_guide_result
from app.config.log import get_logger
from app.database.models import User
from app.modules.musicocean.enums import Engine
from app.modules.musicocean.exceptions import ProviderDataException, ProviderException
from app.modules.musicocean_tg import TelegramMusicOceanClient
from app.modules.musicocean_tg.utils import prefix_to_engine

logger = get_logger(__name__)

router = Router()


@router.inline_query(F.query.regexp(r'^(dz|sc|yt|sp)::(al|ar|pl)::([A-Za-z0-9_-]+)$'))
async def inline_query(
        query: InlineQuery,
        musicocean: FromDishka[TelegramMusicOceanClient],
        user: User,
        i18n: I18nContext
):
    engine_prefix, entity_prefix, entity_id = query.query.split('::', maxsplit=2)
    logger.info(f"User #{query.from_user.id} searched for \"{query.query}\"")

    # todo :=
    try:
        engine = prefix_to_engine(engine_prefix)
    except ValueError:
        await query.answer(usage_guide_result())
        return

    if engine in (Engine.DEEZER, Engine.SOUNDCLOUD):
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
    except ProviderDataException:
        logger.debug("No data for that query")
        return
    except ProviderException as e:
        # spotify answers 403 for an artist's tracks under client credentials;
        # an unanswered inline query just spins, so say what happened instead
        logger.warning(f"{entity_prefix} tracks failed on {engine.value} {entity_id}: {e!r}")
        await query.answer(
            not_supported_result(i18n.get('feature-entity-tracks')),
            cache_time=0
        )
        return

    logger.debug(f"matches: {matches}")

    await query.answer(
        await get_track_results(engine, matches, user.settings.track_preview_covers),
        cache_time=0,
        is_personal=True
    )
