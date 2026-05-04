from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.constants import BACK_EMOJI_ID
from app.bot.callbacks.mailing_callback import MailingCallback
from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath


def mailing_message_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="Back",
            callback_data=MainMenuCallback(path=MainMenuPath.ADMIN_PANEL).pack(),
            icon_custom_emoji_id=BACK_EMOJI_ID
        )
    ]])

def mailing_approve_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Send",
            callback_data=MailingCallback(approved=True).pack(),
        )],
        [InlineKeyboardButton(
            text="Cancel",
            callback_data=MailingCallback(approved=False).pack(),
        )]
    ])