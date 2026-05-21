from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext

from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath
from app.bot.keyboards import guide_keyboard
from app.config import settings

router = Router()


@router.callback_query(MainMenuCallback.filter(F.path == MainMenuPath.GUIDE))
async def usage_guide(callback: CallbackQuery, i18n: I18nContext):
    await callback.message.edit_text(
        text=i18n.get('usage-guide-text', guide_url=settings.local.guide_url),
        reply_markup=guide_keyboard(),
        disable_web_page_preview=True
    )
