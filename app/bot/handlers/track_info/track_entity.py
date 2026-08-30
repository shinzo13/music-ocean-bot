import html

from aiogram import Bot, Router
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext
from dishka import FromDishka

from app.bot.callbacks.track_entity_callback import TrackEntity, TrackEntityCallback
from app.bot.keyboards.entity_keyboard import entity_keyboard
from app.config.log import get_logger
from app.modules.musicocean.enums import Engine
from app.modules.musicocean.exceptions import MusicOceanException
from app.modules.musicocean_tg import TelegramMusicOceanClient
from app.modules.musicocean_tg.utils import prefix_to_engine

logger = get_logger(__name__)

router = Router()

# yandex track ids are strings, the rest are numeric
STRING_ID_ENGINES = (Engine.YOUTUBE, Engine.SPOTIFY, Engine.YANDEX)


@router.callback_query(TrackEntityCallback.filter())
async def track_entity(
        callback: CallbackQuery,
        callback_data: TrackEntityCallback,
        bot: Bot,
        musicocean: FromDishka[TelegramMusicOceanClient],
        i18n: I18nContext,
):
    """Opens the album or the artist a track belongs to.

    The answer looks exactly like an inline search result for that entity, so a
    track found in a chat leads to the same place as a search for it would.
    """
    try:
        engine = prefix_to_engine(callback_data.engine_prefix)
    except ValueError:
        await callback.answer(i18n.get('entity-not-available'), show_alert=True)
        return

    track_id: int | str = callback_data.track_id
    if engine not in STRING_ID_ENGINES:
        try:
            track_id = int(track_id)
        except ValueError:
            await callback.answer(i18n.get('entity-not-available'), show_alert=True)
            return

    is_album = callback_data.entity is TrackEntity.ALBUM

    try:
        track = await musicocean.get_track(engine, track_id)
    except MusicOceanException as e:
        # an engine that cannot even describe its own track (youtube) says so in
        # the alert rather than leaving the button looking broken
        logger.warning(f"track lookup failed for {engine.value} {track_id}: {e!r}")
        await callback.answer(i18n.get('entity-not-available'), show_alert=True)
        return

    entity_id = track.album_id if is_album else track.artist_id
    if entity_id is None:
        await callback.answer(
            i18n.get('entity-album-unknown' if is_album else 'entity-artist-unknown'),
            show_alert=True
        )
        return

    try:
        entity = (
            await musicocean.get_album(engine, entity_id) if is_album
            else await musicocean.get_artist(engine, entity_id)
        )
    except Exception as e:  # noqa: BLE001 — an engine may not implement this at all
        logger.warning(f"{callback_data.entity} lookup failed on {engine.value} {entity_id}: {e!r}")
        await callback.answer(i18n.get('entity-not-available'), show_alert=True)
        return

    if entity is None:
        await callback.answer(i18n.get('entity-not-available'), show_alert=True)
        return

    if is_album:
        text = i18n.get(
            'entity-album',
            title=html.escape(entity.title),
            artist_name=html.escape(entity.artist_name),
            cover_url=entity.cover_url
        )
    else:
        text = i18n.get(
            'entity-artist',
            name=html.escape(entity.name),
            listeners=entity.listeners,
            cover_url=entity.photo_url
        )

    await callback.answer()
    await callback.message.answer(
        text,
        reply_markup=entity_keyboard(
            engine=engine,
            bot_username=(await bot.get_me()).username,
            entity_id=entity_id,
            prefix=callback_data.entity.value,
            download_all=is_album
        )
    )
