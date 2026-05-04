from aiogram import Router, F
from aiogram.types import CallbackQuery
from dishka import FromDishka

from app.bot.constants import PROFILE_EMOJI
from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath
from app.bot.keyboards import profile_keyboard
from app.database.models import User
from app.database.repositories import UserRepository

router = Router()

@router.callback_query(MainMenuCallback.filter(F.path==MainMenuPath.PROFILE))
async def user_profile(
        callback: CallbackQuery,
        user: User,
        user_repo: FromDishka[UserRepository],
):
    downloaded_tracks = await user_repo.get_user_downloaded_tracks(user.user_id)
    text = (
        f"<b>{PROFILE_EMOJI} {callback.from_user.mention_html()}</b>\n\n"
        f"<b>• Registered</b>: <code>{user.created_at.strftime("%Y-%m-%d")}</code>\n"
        f"<b>• Tracks downloaded</b>: <code>{len(downloaded_tracks)}</code>"
    )
    await callback.message.edit_text(
        text=text,
        reply_markup=profile_keyboard()
    )
