from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# TODO back_home_kb if here would be no more content
def guide_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="⬅️ Back", callback_data="main_menu")
    ]])