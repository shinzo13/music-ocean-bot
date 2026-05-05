from sys import prefix

from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext
from dishka import FromDishka

from app.bot.callbacks.default_engine_callback import DefaultEngineCallback
from app.bot.callbacks.settings_callback import SettingsCallback, SettingsPath
from app.database.models import User
from app.bot.keyboards import engines_keyboard
from app.database.repositories import UserRepository
from app.modules.musicocean.enums import Engine
from app.modules.musicocean_tg.utils import prefix_to_engine


router = Router()

@router.callback_query(SettingsCallback.filter(F.path==SettingsPath.ENGINE))
async def default_engine_handler(callback: CallbackQuery, user: User, i18n: I18nContext):
    await callback.message.edit_text(
        text=i18n.get('choose-engine'),
        reply_markup=engines_keyboard(user.settings.selected_engine)
    )

@router.callback_query(DefaultEngineCallback.filter())
async def set_engine_handler(
        query: CallbackQuery,
        callback_data: DefaultEngineCallback,
        user: User,
        i18n: I18nContext,
        user_repo: FromDishka[UserRepository],
):
    engine = prefix_to_engine(callback_data.engine_prefix)

    if user.settings.selected_engine == engine:
        await query.answer(i18n.get('option-already-selected'), show_alert=True)
        return

    user: await user_repo.update_user_settings(
        user_id=user.user_id,
        selected_engine=engine
    )
    await query.message.edit_reply_markup(
        reply_markup=engines_keyboard(user.settings.selected_engine)
    )

    await query.answer(i18n.get('engine-changed'))