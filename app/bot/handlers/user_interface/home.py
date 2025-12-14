from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from app.bot.keyboards import home_keyboard

router = Router()

@router.message(CommandStart(deep_link=False))
async def main_menu(message: Message):
    await message.answer(
        text="Welcome to Music Ocean!",
        reply_markup=home_keyboard()
    )

@router.callback_query(F.data=="main_menu")
async def main_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Welcome to Music Ocean!",
        reply_markup=home_keyboard()
    )