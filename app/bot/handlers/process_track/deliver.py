from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Chat, InputMediaAudio, User
from aiogram_i18n import I18nContext

from app.bot.keyboards.download_button import downloading_keyboard
from app.bot.utils.admin_notify import notify_admins_track
from app.bot.utils.save_track import save_track_with_source
from app.bot.utils.track_ref import TrackRef
from app.config.log import get_logger
from app.config.settings import settings
from app.database.repositories import TrackRepository, UserRepository
from app.modules.musicocean_tg import TelegramMusicOceanClient

logger = get_logger(__name__)

# inline messages already being served: the chosen-result update and a button
# press can arrive for the same message, and downloading a track twice would
# post it to the channel twice as well
_in_flight: set[str] = set()


def is_in_flight(inline_message_id: str) -> bool:
    return inline_message_id in _in_flight


async def deliver_track(
        ref: TrackRef,
        inline_message_id: str,
        requester: User | Chat,
        bot: Bot,
        musicocean: TelegramMusicOceanClient,
        track_repo: TrackRepository,
        user_repo: UserRepository,
        i18n: I18nContext,
) -> None:
    if inline_message_id in _in_flight:
        logger.debug(f"already delivering {ref.engine.value} {ref.track_id}")
        return
    _in_flight.add(inline_message_id)
    try:
        await _deliver(ref, inline_message_id, requester, bot, musicocean, track_repo, user_repo, i18n)
    finally:
        _in_flight.discard(inline_message_id)


async def _deliver(
        ref: TrackRef,
        inline_message_id: str,
        requester: User | Chat,
        bot: Bot,
        musicocean: TelegramMusicOceanClient,
        track_repo: TrackRepository,
        user_repo: UserRepository,
        i18n: I18nContext,
) -> None:
    db_track = await track_repo.get_track(ref.track_id, ref.engine)
    if db_track:
        try:
            await bot.edit_message_media(
                media=InputMediaAudio(media=db_track.telegram_file_id),
                inline_message_id=inline_message_id
            )
            logger.info(f"Successfully sent cached track #{ref.engine.value} {ref.track_id}")
        except TelegramBadRequest as e:
            logger.warning(f"edit failed for cached {ref.track_id}: {e.message}")
        return

    # the button says "downloading" for as long as the download runs, so a slow
    # track does not look like a dead one
    try:
        await bot.edit_message_reply_markup(
            inline_message_id=inline_message_id,
            reply_markup=downloading_keyboard()
        )
    except TelegramBadRequest:
        pass

    try:
        cached = await musicocean.download_track(engine=ref.engine, track_id=ref.track_id)
    except Exception as e:  # noqa: BLE001 — source may 404/geoblock/remove a track
        logger.warning(f"download failed for {ref.engine.value} {ref.track_id}: {e!r}")
        try:
            await bot.edit_message_text(
                inline_message_id=inline_message_id,
                text=i18n.get('error-track-unavailable') + "\n\n" + i18n.get('support-hint'),
            )
        except TelegramBadRequest as edit_err:
            logger.warning(f"error edit failed for {ref.track_id}: {edit_err.message}")
        return

    file_id = cached.file_id
    logger.debug(f"got file id: {file_id}")
    try:
        await bot.edit_message_media(
            media=InputMediaAudio(media=file_id),
            inline_message_id=inline_message_id
        )
        logger.info(f"Successfully sent track #{ref.engine.value} {ref.track_id}")
    except TelegramBadRequest as e:
        logger.warning(f"edit failed for {ref.track_id}: {e.message}")

    # telegram caching causing this shi
    if await track_repo.get_track(ref.track_id, ref.engine) is None:
        await save_track_with_source(
            track_repo,
            engine=ref.engine,
            track_id=ref.track_id,
            cached=cached,
            file_id=file_id,
            file_unique_id=cached.file_unique_id,
            user_id=requester.id,
            download_context=ref.download_context,
            entity_type=ref.entity_type,
            download_mode=ref.download_mode
        )
        notify_admins = await user_repo.get_notify_admin_ids(settings.telegram.admins)
        await notify_admins_track(
            bot, notify_admins,
            ref.engine, cached.artist_name, cached.title,
            ref.track_id, requester
        )
