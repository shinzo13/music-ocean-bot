from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext

from app.bot.handlers.user_interface.home import MainMenuCallback, MainMenuPath
from app.bot.keyboards import admin_panel_keyboard

router = Router()


@router.callback_query(MainMenuCallback.filter(F.path == MainMenuPath.ADMIN_PANEL))
async def admin_panel(callback: CallbackQuery, i18n: I18nContext):
    await callback.message.edit_text(
        text=i18n.get('admin-panel-text'),
        reply_markup=admin_panel_keyboard()
    )
