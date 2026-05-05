from enum import StrEnum, auto

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram_i18n import I18nContext

from app.bot.handlers.user_interface.home import MainMenuCallback, MainMenuPath
from app.bot.keyboards import home_keyboard, admin_panel_keyboard
from app.database.models import User


router = Router()

@router.callback_query(MainMenuCallback.filter(F.path==MainMenuPath.ADMIN_PANEL))
async def admin_panel(callback: CallbackQuery, i18n: I18nContext):
    await callback.message.edit_text(
        text=i18n.get('admin-panel-text'),
        reply_markup=admin_panel_keyboard()
    )