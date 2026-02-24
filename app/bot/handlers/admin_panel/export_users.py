from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, BufferedInputFile
from dishka import FromDishka
from datetime import datetime
from app.bot.keyboards import home_keyboard
from app.database.models import User
from app.database.repositories import UserRepository

router = Router()

@router.callback_query(F.data=="users")
async def main_menu(callback: CallbackQuery, user_repo: FromDishka[UserRepository]):
    csv_bytes = await user_repo.export_to_csv()
    timestamp = datetime.now().strftime("%Y-%m-%d")
    await callback.message.answer_document(
        document=BufferedInputFile(
            file=csv_bytes,
            filename=f"users-{timestamp}.csv"
        )
    )