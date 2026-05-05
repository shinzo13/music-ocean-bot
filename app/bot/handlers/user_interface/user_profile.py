from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext
from dishka import FromDishka

from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath
from app.bot.keyboards import profile_keyboard
from app.database.models import User
from app.database.repositories import UserRepository

router = Router()


@router.callback_query(MainMenuCallback.filter(F.path == MainMenuPath.PROFILE))
async def user_profile(
        callback: CallbackQuery,
        user: User,
        user_repo: FromDishka[UserRepository],
        i18n: I18nContext
):
    downloaded_tracks = await user_repo.get_user_downloaded_tracks(user.user_id)
    text = i18n.get(
        'profile-text',
        user=callback.from_user.mention_html(),
        registered=user.created_at.strftime("%Y-%m-%d"),
        tracks_downloaded=len(downloaded_tracks)
    )
    await callback.message.edit_text(
        text=text,
        reply_markup=profile_keyboard()
    )
