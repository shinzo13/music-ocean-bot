from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from dishka import FromDishka

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
        reply_markup=engines_keyboard(user.selected_engine)
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

    if user.selected_engine == engine:
        await callback.answer("This engine is already selected.", show_alert=True)
        return

    user = await user_repo.update_user(
        user_id=user.user_id,
        selected_engine=engine
    )
    await callback.message.edit_reply_markup(
        reply_markup=engines_keyboard(user.selected_engine) # noqa
    )

    await callback.answer("✅ Engined changed successfully.")
