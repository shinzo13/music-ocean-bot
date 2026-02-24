from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def mailing_message_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="⬅️ Back", callback_data="admin")
    ]])

def mailing_approve_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Approve", callback_data="mailing_approve")],
        [InlineKeyboardButton(text="Cancel", callback_data="mailing_cancel")]
    ])