from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def home_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="How to use?", callback_data="usage_guide")],
        [
            InlineKeyboardButton(text="Profile", callback_data="profile"),
            InlineKeyboardButton(text="Settings", callback_data="settings")
        ]
    ])