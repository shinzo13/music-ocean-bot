from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def settings_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Default engine", callback_data="default_engine")],
        [InlineKeyboardButton(text="Track preview appearance", callback_data="track_preview_appearance")],
        [InlineKeyboardButton(text="⬅️ Back", callback_data="main_menu")]
    ])