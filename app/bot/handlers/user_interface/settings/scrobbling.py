from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from dishka import FromDishka

from app.bot.callbacks.settings_callback import SettingsCallback, SettingsPath
from app.bot.callbacks.setup_scrobbling_callback import SetupScrobblingCallback
from app.bot.keyboards.scrobbling import scrobbling_setup_keyboard, scrobbling_cancel_keyboard
from app.bot.keyboards.scrobbling.scrobbling_approve_keyboard import scrobbling_approve_keyboard
from app.database.models import User
from app.database.repositories import UserRepository
from app.modules.musicocean.exceptions import MusicOceanException
from app.modules.musicocean_tg import TelegramMusicOceanClient


class ScrobblingSetupState(StatesGroup):
    lastfm_username = State()
    approving = State()


router = Router()


@router.callback_query(SettingsCallback.filter(F.path==SettingsPath.SCROBBLING))
async def spotify_scrobbling_handler(
        callback: CallbackQuery,
        user: User
):
    if user.settings.lastfm.enabled:
        await callback.message.edit_text(
            "already"  # TODO
        )
        return

    await callback.message.edit_text(
        f"<b>Spotify scrobbling</b>\n\nLog in into your Spotify account and get ability to quickly download tracks from your player.",
        reply_markup=scrobbling_setup_keyboard()
    )


@router.callback_query(SetupScrobblingCallback.filter(F.init))
async def setup_scrobbling_handler_init(
        query: CallbackQuery,
        state: FSMContext,
):
    await state.set_state(ScrobblingSetupState.lastfm_username)
    await query.message.edit_text(
        "enter lastfm username"
    )

@router.message(ScrobblingSetupState.lastfm_username)
async def setup_scrobbling_handler_username(
        message: Message,
        state: FSMContext,
        musicocean: FromDishka[TelegramMusicOceanClient]
):
    lastfm_username = message.text
    if not await musicocean.lastfm.check_user(lastfm_username):
        await message.answer(
            "invalid username, try again",
            reply_markup=scrobbling_cancel_keyboard()
        )
        return

    try:
        engine, track = await musicocean.lastfm.get_recent_track_data(lastfm_username)
    except: #todo
        await message.answer(
            "no data available",
            reply_markup = scrobbling_cancel_keyboard()
        )
        return

    await message.answer(
        f"last track: <i>{track.artist_name} - {track.title}</i>\n\nis that right??",
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
        user_repo: FromDishka[UserRepository]
):
    if callback_data.approved:
        await user_repo.update_user_settings(
            user_id=query.from_user.id,
            lastfm__enabled=True,
            lastfm__username=await state.get_value('lastfm_username')
        )
        await query.message.edit_text(
            "successfully setup lastfm scrobbling.",
            reply_markup=scrobbling_setup_keyboard()
        )