from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from app.bot.keyboards import home_keyboard
from app.database.models import User

router = Router()

@router.message(CommandStart(deep_link=False))
async def main_menu(message: Message, user: User):
    await message.answer(
        text=f"Welcome to <b>Music Ocean!</b> 🌊",
        reply_markup=home_keyboard(user.is_admin)
    )

@router.callback_query(F.data=="main_menu")
async def main_menu(callback: CallbackQuery, user: User):
    await callback.message.edit_text(
        text="Welcome to <b>Music Ocean!</b> 🌊",
        reply_markup=home_keyboard(user.is_admin)
    )