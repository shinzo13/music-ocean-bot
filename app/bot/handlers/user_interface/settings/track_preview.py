from aiogram import Router, F, Bot
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery
from dishka import FromDishka

from app.bot.callbacks.settings_callback import SettingsCallback, SettingsPath
from app.bot.callbacks.track_previews_callback import TrackPreviewsCallback
from app.bot.keyboards.track_preview_keyboard import track_preview_keyboard
from app.database.models import User
from app.database.repositories import UserRepository



router = Router()

@router.callback_query(SettingsCallback.filter(F.path==SettingsPath.PREVIEWS))
async def track_preview_appearance_handler(callback: CallbackQuery, user: User):
    await callback.message.edit_text(
        text="Choose track preview appearance:",
        reply_markup=track_preview_keyboard(user.settings.track_preview_covers)
    )

@router.callback_query(TrackPreviewsCallback.filter())
async def set_previews_handler(
        query: CallbackQuery,
        callback_data: TrackPreviewsCallback,
        user: User,
        user_repo: FromDishka[UserRepository]
):
    if callback_data.show_covers==user.settings.track_preview_covers:
        await query.answer("This option is already selected.", show_alert=True)
        return

    user = await user_repo.update_user_settings(
        user_id=user.user_id,
        track_preview_covers=callback_data.show_covers
    )
    await query.message.edit_reply_markup(
        reply_markup=track_preview_keyboard(user.settings.track_preview_covers)
    )

    await query.answer("✅ Track preview options changed successfully")