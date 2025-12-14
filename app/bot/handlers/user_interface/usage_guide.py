from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from app.bot.keyboards import guide_keyboard


router = Router()

@router.callback_query(F.data=="usage_guide")
async def usage_guide(callback: CallbackQuery, bot: Bot):
    await callback.message.edit_text(
        text="usage guide will be here",
        reply_markup=guide_keyboard()
    )
