from aiogram import Router, F
from aiogram.types import CallbackQuery
from dishka import FromDishka

from app.bot.keyboards.track_preview_keyboard import track_preview_keyboard
from app.database.models import User
from app.bot.keyboards import engines_keyboard, settings_keyboard
from app.database.repositories import UserRepository
from app.modules.musicocean.enums import Engine

router = Router()

@router.callback_query(F.data=="settings")
async def settings_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Settings",
        reply_markup=settings_keyboard()
    )

@router.callback_query(F.data=="default_engine")
async def default_engine_handler(callback: CallbackQuery, user: User):
    await callback.message.edit_text(
        text="Choose a default engine to use:",
        reply_markup=engines_keyboard(user.settings.selected_engine)
    )

@router.callback_query(F.data.startswith("set_engine"))
async def set_engine_handler(
        callback: CallbackQuery,
        user: User,
        user_repo: FromDishka[UserRepository],
):
    engine_prefix = callback.data.removeprefix("set_engine_")
    match engine_prefix:
        case "dz":
            engine = Engine.DEEZER
        case "sc":
            engine = Engine.SOUNDCLOUD
        case "yt":
            engine = Engine.YOUTUBE
        case "sp":
            engine = Engine.SPOTIFY
        case _:
            raise

    if user.settings.selected_engine == engine:
        await callback.answer("This engine is already selected.", show_alert=True)
        return

    user: User = await user_repo.update_user_settings(
        user_id=user.user_id,
        selected_engine=engine
    )
    await callback.message.edit_reply_markup(
        reply_markup=engines_keyboard(user.settings.selected_engine)
    )

    await callback.answer("✅ Engined changed successfully.")

@router.callback_query(F.data=="track_preview_appearance")
async def track_preview_appearance_handler(callback: CallbackQuery, user: User):
    await callback.message.edit_text(
        text="Choose track preview appearance:",
        reply_markup=track_preview_keyboard(user.settings.track_preview_covers)
    )

@router.callback_query(F.data.startswith("set_previews_"))
async def set_previews_handler(
        callback: CallbackQuery,
        user: User,
        user_repo: FromDishka[UserRepository]
):
    show_covers = True if callback.data.removeprefix("set_previews_")=="covers" else False
    if show_covers==user.settings.track_preview_covers:
        await callback.answer("This option id already selected.", show_alert=True)
        return

    user: User = await user_repo.update_user_settings(
        user_id=user.user_id,
        track_preview_covers=show_covers
    )
    await callback.message.edit_reply_markup(
        reply_markup=track_preview_keyboard(user.settings.track_preview_covers)
    )

    await callback.answer("✅ Track preview options changed successfully.")