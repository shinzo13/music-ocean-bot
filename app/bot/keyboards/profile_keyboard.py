from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.constants import BACK_EMOJI_ID


def profile_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="Back",
            callback_data="main_menu",
            icon_custom_emoji_id=BACK_EMOJI_ID
        )
    ]])