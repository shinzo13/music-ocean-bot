from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from app.bot.keyboards import home_keyboard, admin_panel_keyboard
from app.database.models import User

router = Router()

@router.callback_query(F.data=="admin")
async def main_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text="admin panel",
        reply_markup=admin_panel_keyboard()
    )