from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.constants import BACK_EMOJI_ID
from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath


def profile_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="Back",
            callback_data=MainMenuCallback(path=MainMenuPath.SELF).pack(),
            icon_custom_emoji_id=BACK_EMOJI_ID
        )
    ]])