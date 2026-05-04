from enum import StrEnum, auto

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from app.bot.handlers.user_interface.home import MainMenuCallback, MainMenuPath
from app.bot.keyboards import home_keyboard, admin_panel_keyboard
from app.database.models import User


router = Router()

@router.callback_query(MainMenuCallback.filter(F.path==MainMenuPath.ADMIN_PANEL))
async def admin_panel(callback: CallbackQuery):
    await callback.message.edit_text(
        text="admin panel",
        reply_markup=admin_panel_keyboard()
    )