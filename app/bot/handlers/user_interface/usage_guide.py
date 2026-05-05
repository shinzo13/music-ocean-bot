from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext

from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath
from app.bot.keyboards import guide_keyboard


router = Router()

@router.callback_query(MainMenuCallback.filter(F.path==MainMenuPath.GUIDE))
async def usage_guide(callback: CallbackQuery, i18n: I18nContext):
    await callback.message.edit_text(
        text=i18n.get('usage-guide-text'),
        reply_markup=guide_keyboard()
    )