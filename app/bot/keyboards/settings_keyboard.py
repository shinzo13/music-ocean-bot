from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def settings_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Default engine", callback_data="default_engine")],
        [InlineKeyboardButton(text="⬅️ Back", callback_data="main_menu")]
    ])