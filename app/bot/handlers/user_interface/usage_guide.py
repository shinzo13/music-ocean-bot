from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath
from app.bot.keyboards import guide_keyboard


router = Router()

@router.callback_query(MainMenuCallback.filter(F.path==MainMenuPath.GUIDE))
async def usage_guide(callback: CallbackQuery, bot: Bot):
    await callback.message.edit_text(
        text="usage guide will be here",
        reply_markup=guide_keyboard()
    )
