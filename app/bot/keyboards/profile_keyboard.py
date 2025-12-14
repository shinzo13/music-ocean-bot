from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def profile_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="⬅️ Back", callback_data="main_menu")
    ]])