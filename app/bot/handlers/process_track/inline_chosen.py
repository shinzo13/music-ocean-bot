from aiogram import Router, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ChosenInlineResult
from aiogram.types import InputMediaAudio
from dishka import FromDishka

from app.bot.utils.admin_notify import notify_admins_track
from app.bot.utils.context_codes import CTX_CODES
from app.config.log import get_logger
from app.config.settings import settings
from app.database.models.download_context import DownloadContext
from app.database.repositories import TrackRepository
from app.modules.musicocean.enums.engine import Engine
from app.modules.musicocean_tg import TelegramMusicOceanClient

logger = get_logger(__name__)

router = Router()


@router.chosen_inline_result()
async def idklol(
        chosen: ChosenInlineResult,
        bot: Bot,
        musicocean: FromDishka[TelegramMusicOceanClient],
        track_repo: FromDishka[TrackRepository]
):
    # todo
    if chosen.result_id in ['usage_guide', "setup_scrobbling"]:
        return
    # todo i hate stupid split i wanna regex in handler
    parts = chosen.result_id.split("_", maxsplit=3)
    if len(parts) < 3 or parts[1] != "tr":
        return
    engine_prefix = parts[0]
    # new ids carry a context code ({engine}_tr_{ctx}_{id}); ids cached by
    # telegram before the rollout lack it — treat those as plain search
    if len(parts) == 4 and parts[2] in CTX_CODES:
        download_context, entity_kind, download_mode = CTX_CODES[parts[2]]
        entity_id = parts[3]
    else:
        download_context, entity_kind, download_mode = DownloadContext.SEARCH, None, None
        entity_id = chosen.result_id.split("_", maxsplit=2)[2]

    match engine_prefix:
        case "dz":
            engine = Engine.DEEZER
            entity_id = int(entity_id)
        case "sc":
            engine = Engine.SOUNDCLOUD
            entity_id = int(entity_id)
        case "yt":
            engine = Engine.YOUTUBE
        case "sp":
            engine = Engine.SPOTIFY
        case "ya":
            engine = Engine.YANDEX
        case _:
            raise "invalid engine"

    db_track = await track_repo.get_track(entity_id, engine)
    if db_track:
        try:
            await bot.edit_message_media(
                media=InputMediaAudio(media=db_track.telegram_file_id),
                inline_message_id=chosen.inline_message_id
            )
            logger.info(f"Successfully sent cached track #{chosen.result_id}")
        except TelegramBadRequest as e:
            logger.warning(f"edit failed for cached #{chosen.result_id}: {e.message}")
        return

    cached = await musicocean.download_track(
        engine=engine,
        track_id=entity_id,
    )
    file_id = cached.file_id
    logger.debug(f"got file id: {file_id}")
    try:
        await bot.edit_message_media(
            media=InputMediaAudio(media=file_id),
            inline_message_id=chosen.inline_message_id
        )
        logger.info(f"Successfully sent track #{chosen.result_id}")
    except TelegramBadRequest as e:
        logger.warning(f"edit failed for #{chosen.result_id}: {e.message}")

    # telegram caching causing this shi
    db_track = await track_repo.get_track(entity_id, engine)
    if db_track is None:
        await track_repo.add_track(
            engine=engine,
            track_id=entity_id,
            telegram_file_id=file_id,
            telegram_file_unique_id=cached.file_unique_id,
            user_id=chosen.from_user.id,
            download_context=download_context,
            entity_type=entity_kind,
            download_mode=download_mode
        )
        await notify_admins_track(
            bot, settings.telegram.admins,
            engine, cached.artist_name, cached.title,
            entity_id, chosen.from_user
        )

    return
