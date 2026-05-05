from aiogram import Router, F, Bot
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext
from dishka import FromDishka

from app.bot.callbacks.locales_callback import LocalesCallback
from app.bot.callbacks.settings_callback import SettingsCallback, SettingsPath
from app.bot.callbacks.track_previews_callback import TrackPreviewsCallback
from app.bot.keyboards.locales_keyboard import locales_keyboard
from app.bot.keyboards.track_preview_keyboard import track_preview_keyboard
from app.database.models import User
from app.database.repositories import UserRepository



router = Router()

@router.callback_query(SettingsCallback.filter(F.path==SettingsPath.LOCALE))
async def track_preview_appearance_handler(
        callback: CallbackQuery,
        user: User,
        i18n: I18nContext
):
    await callback.message.edit_text(
        text=i18n.get('choose-language'),
        reply_markup=locales_keyboard(user.settings.locale)
    )

@router.callback_query(LocalesCallback.filter())
async def set_previews_handler(
        query: CallbackQuery,
        callback_data: LocalesCallback,
        user: User,
        user_repo: FromDishka[UserRepository],
        i18n: I18nContext
):
    if callback_data.code==user.settings.locale:
        await query.answer(i18n.get('option-already-selected'), show_alert=True)
        return

    user = await user_repo.update_user_settings(
        user_id=user.user_id,
        locale=callback_data.code
    )
    await i18n.set_locale(user.settings.locale)
    await query.message.edit_text(
        text=i18n.get('choose-language'),
        reply_markup=locales_keyboard(user.settings.locale)
    )

    await query.answer(i18n.get('language-changed'))