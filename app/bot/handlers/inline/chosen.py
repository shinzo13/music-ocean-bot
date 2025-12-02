from aiogram import Router, F, Bot
from aiogram.types import ChosenInlineResult
from aiogram.types import InputMediaAudio
from dishka import FromDishka

from app.database.repositories import TrackRepository
from app.modules.musicocean_tg import TelegramMusicOceanClient
from app.config.log import get_logger
from app.modules.musicocean.enums import Engine


logger = get_logger(__name__)

router = Router()



@router.chosen_inline_result()
async def idklol(
        chosen: ChosenInlineResult,
        bot: Bot,
        musicocean: FromDishka[TelegramMusicOceanClient],
        track_repo: FromDishka[TrackRepository]
):
    if chosen.result_id.startswith("cached"):
        return None

    engine_prefix, entity_type, entity_id = chosen.result_id.split("_")
    entity_id = int(entity_id)
    if entity_type != "tr":
        return None

    match engine_prefix:
        case "dz":
            engine = Engine.DEEZER
        case "sc":
            engine = Engine.SOUNDCLOUD
        case "yt":
            engine = Engine.YOUTUBE
        case "sp":
            engine = Engine.SPOTIFY
        case _:
            raise "invalid engine"

    file_id = await musicocean.download_track(
        engine=engine,
        track_id=entity_id,
    )

    await bot.edit_message_media(
        media=InputMediaAudio(media=file_id),
        inline_message_id=chosen.inline_message_id
    )
    logger.info(f"Successfully sent track #{chosen.result_id}")

    # telegram caching causing this shi
    db_track = await track_repo.get_track_by_id(entity_id)
    if db_track is None:
        await track_repo.add_track(
            engine=engine,
            track_id=entity_id,
            telegram_file_id=file_id,
            user_id=chosen.from_user.id
        )

    return None