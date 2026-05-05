from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from dishka import FromDishka

from app.bot.callbacks.settings_callback import SettingsCallback, SettingsPath
from app.bot.callbacks.setup_scrobbling_callback import SetupScrobblingCallback
from app.bot.keyboards.scrobbling import scrobbling_setup_keyboard, scrobbling_cancel_keyboard
from app.bot.keyboards.scrobbling.scrobbling_approve_keyboard import scrobbling_approve_keyboard
from app.database.models import User
from app.database.repositories import UserRepository
from app.modules.musicocean.exceptions import MusicOceanException
from app.modules.musicocean.lastfm.exceptions import LastFMNoDataException
from app.modules.musicocean_tg import TelegramMusicOceanClient
from app.config.log import get_logger

logger = get_logger(__name__)

class ScrobblingSetupState(StatesGroup):
    lastfm_username = State()
    approving = State()


router = Router()


@router.callback_query(SettingsCallback.filter(F.path==SettingsPath.SCROBBLING))
async def spotify_scrobbling_handler(
        callback: CallbackQuery,
        user: User,
        i18n: I18nContext
):
    if user.settings.lastfm.enabled:
        await callback.message.edit_text(
            i18n.get('scrobbling-already-setup'),  # TODO
            reply_markup=scrobbling_setup_keyboard(again=True)
        )
    else:
        await callback.message.edit_text(
            i18n.get('scrobbling-description'),
            reply_markup=scrobbling_setup_keyboard()
        )

@router.message(
    CommandStart(
        deep_link=True,
        magic=F.args.regexp('setup_scrobbling')
    )
)
async def spotify_scrobbling_handler(
        message: Message,
        user: User,
        i18n: I18nContext
):
    if user.settings.lastfm.enabled:
        await message.answer(
            i18n.get('scrobbling-already-setup'),
            reply_markup=scrobbling_setup_keyboard(again=True)
        )
    else:
        await message.answer(
            i18n.get('scrobbling-description'),
            reply_markup=scrobbling_setup_keyboard()
        )



@router.callback_query(SetupScrobblingCallback.filter(F.init))
async def setup_scrobbling_handler_init(
        query: CallbackQuery,
        state: FSMContext,
        i18n: I18nContext
):
    await state.set_state(ScrobblingSetupState.lastfm_username)
    await query.message.edit_text(
        i18n.get('scrobbling-enter-username')
    )

@router.message(ScrobblingSetupState.lastfm_username and F.text)
async def setup_scrobbling_handler_username(
        message: Message,
        state: FSMContext,
        musicocean: FromDishka[TelegramMusicOceanClient],
        i18n: I18nContext
):
    lastfm_username = message.text
    logger.debug(f"lastfm username: {lastfm_username}")
    if lastfm_username == "":
        return
    if not await musicocean.lastfm.check_user(lastfm_username):
        await message.answer(
            i18n.get('scrobbling-invalid-username'),
            reply_markup=scrobbling_cancel_keyboard()
        )
        return

    try:
        track_data = await musicocean.lastfm.get_recent_track_data(lastfm_username)
    except LastFMNoDataException: #todo
        await message.answer(
            i18n.get('scrobbling-no-data'),
            reply_markup = scrobbling_cancel_keyboard()
        )
        return

    await message.answer(
        i18n.get(
            'scrobbling-is-that-right',
            artist=track_data.artist_name,
            title=track_data.title
        ),
        reply_markup=scrobbling_approve_keyboard()
    )
    await state.update_data(lastfm_username=lastfm_username)
    await state.set_state(ScrobblingSetupState.approving)

@router.callback_query(SetupScrobblingCallback.filter(~F.init))
async def setup_scrobbling_handler_approve(
        query: CallbackQuery,
        callback_data: SetupScrobblingCallback,
        state: FSMContext,
        musicocean: FromDishka[TelegramMusicOceanClient],
        user_repo: FromDishka[UserRepository],
        i18n: I18nContext
):
    if callback_data.approved:
        await user_repo.update_user_settings(
            user_id=query.from_user.id,
            lastfm__enabled=True,
            lastfm__username=await state.get_value('lastfm_username')
        )
        await query.message.edit_text(
            i18n.get('scrobbling-success'),
            reply_markup=scrobbling_setup_keyboard()
        )