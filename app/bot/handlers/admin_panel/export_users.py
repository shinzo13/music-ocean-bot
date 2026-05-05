from datetime import datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery, BufferedInputFile
from dishka import FromDishka

from app.bot.callbacks.admin_panel_callback import AdminPanelCallback, AdminPanelPath
from app.database.repositories import UserRepository

router = Router()


@router.callback_query(AdminPanelCallback.filter(F.path == AdminPanelPath.EXPORT_USERS))
async def main_menu(callback: CallbackQuery, user_repo: FromDishka[UserRepository]):
    csv_bytes = await user_repo.export_to_csv()
    timestamp = datetime.now().strftime("%Y-%m-%d")
    await callback.message.answer_document(
        document=BufferedInputFile(
            file=csv_bytes,
            filename=f"users-{timestamp}.csv"
        )
    )
