from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext

from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath
from app.bot.keyboards import home_keyboard
from app.database.models import User

router = Router()


@router.message(CommandStart(deep_link=False))
async def main_menu_from_message(message: Message, user: User, i18n: I18nContext):
    await message.answer(
        text=i18n.get('welcome'),
        reply_markup=home_keyboard(user.is_admin)
    )


@router.callback_query(MainMenuCallback.filter(F.path == MainMenuPath.SELF))
async def main_menu_from_callback(callback: CallbackQuery, user: User, i18n: I18nContext):
    await callback.message.edit_text(
        text=i18n.get('welcome'),
        reply_markup=home_keyboard(user.is_admin)
    )
