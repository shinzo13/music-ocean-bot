from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, ChosenInlineResult
from aiogram_i18n import I18nContext
from dishka import FromDishka

from app.bot.handlers.process_track.deliver import deliver_track, is_in_flight
from app.bot.utils.track_ref import parse_track_ref
from app.config.log import get_logger
from app.database.repositories import TrackRepository, UserRepository
from app.modules.musicocean_tg import TelegramMusicOceanClient

logger = get_logger(__name__)

router = Router()


@router.chosen_inline_result()
async def idklol(
        chosen: ChosenInlineResult,
        bot: Bot,
        musicocean: FromDishka[TelegramMusicOceanClient],
        track_repo: FromDishka[TrackRepository],
        user_repo: FromDishka[UserRepository],
        i18n: I18nContext,
):
    # logged before anything is parsed: telegram delivering no update at all and
    # an id we failed to read used to look identical in the log — like nothing
    logger.info(f"chosen inline result #{chosen.result_id} by {chosen.from_user.id}")

    ref = parse_track_ref(chosen.result_id)
    if ref is None:
        return
    if not chosen.inline_message_id:
        # no reply markup means no message to edit: nothing to deliver into
        logger.warning(f"no inline_message_id for #{chosen.result_id}")
        return

    await deliver_track(
        ref, chosen.inline_message_id, chosen.from_user,
        bot, musicocean, track_repo, user_repo, i18n
    )


@router.callback_query(F.data.regexp(r'^(dz|sc|yt|sp|ya)_tr_'))
async def download_button(
        callback: CallbackQuery,
        bot: Bot,
        musicocean: FromDishka[TelegramMusicOceanClient],
        track_repo: FromDishka[TrackRepository],
        user_repo: FromDishka[UserRepository],
        i18n: I18nContext,
):
    """The manual path. Telegram feeds chosen_inline_result only for a share of
    picks, and posting as an anonymous channel drops it entirely — the button is
    what a user has left when the automatic download never starts."""
    ref = parse_track_ref(callback.data or '')
    if ref is None or not callback.inline_message_id:
        await callback.answer()
        return

    if is_in_flight(callback.inline_message_id):
        await callback.answer(i18n.get('btn-downloading'))
        return

    logger.info(f"download button #{callback.data} by {callback.from_user.id}")
    await callback.answer()
    await deliver_track(
        ref, callback.inline_message_id, callback.from_user,
        bot, musicocean, track_repo, user_repo, i18n
    )


# "meow mrrnyaahhhhh" is the pre-button callback data: those messages are still
# sitting in chats, and a press on them must not spin forever
@router.callback_query(F.data.in_({'downloading', 'meow mrrnyaahhhhh'}))
async def already_downloading(callback: CallbackQuery, i18n: I18nContext):
    await callback.answer(i18n.get('btn-downloading'))
