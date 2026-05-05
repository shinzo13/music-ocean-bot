from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext
from dishka import FromDishka

from app.bot.callbacks.settings_callback import SettingsCallback, SettingsPath
from app.bot.callbacks.track_previews_callback import TrackPreviewsCallback
from app.bot.keyboards.track_preview_keyboard import track_preview_keyboard
from app.database.models import User
from app.database.repositories import UserRepository

router = Router()


@router.callback_query(SettingsCallback.filter(F.path == SettingsPath.PREVIEWS))
async def track_preview_appearance_handler(
        callback: CallbackQuery,
        user: User,
        i18n: I18nContext
):
    await callback.message.edit_text(
        text=i18n.get('choose-previews'),
        reply_markup=track_preview_keyboard(i18n, user.settings.track_preview_covers)
    )


@router.callback_query(TrackPreviewsCallback.filter())
async def set_previews_handler(
        query: CallbackQuery,
        callback_data: TrackPreviewsCallback,
        user: User,
        user_repo: FromDishka[UserRepository],
        i18n: I18nContext
):
    if callback_data.show_covers == user.settings.track_preview_covers:
        await query.answer(i18n.get('previews-already-selected'), show_alert=True)
        return

    user = await user_repo.update_user_settings(
        user_id=user.user_id,
        track_preview_covers=callback_data.show_covers
    )
    await query.message.edit_reply_markup(
        reply_markup=track_preview_keyboard(i18n, user.settings.track_preview_covers)
    )

    await query.answer(i18n.get('previews-changed'))
