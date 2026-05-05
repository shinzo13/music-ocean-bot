from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext

from app.bot.handlers.user_interface.home import MainMenuCallback, MainMenuPath
from app.bot.keyboards import settings_keyboard

router = Router()


@router.callback_query(MainMenuCallback.filter(F.path == MainMenuPath.SETTINGS))
async def settings_handler(callback: CallbackQuery, i18n: I18nContext):
    await callback.message.edit_text(
        text=i18n.get('settings-text'),
        reply_markup=settings_keyboard()
    )
    await callback.answer()
