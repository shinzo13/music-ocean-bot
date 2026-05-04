from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.constants import SPOTIFY_EMOJI_ID, BACK_EMOJI_ID
from app.bot.callbacks.setup_scrobbling_callback import SetupScrobblingCallback


def scrobbling_approve_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="Yes",
            callback_data=SetupScrobblingCallback(init=False, approved=True).pack()
        ),
        InlineKeyboardButton(
            text="No",
            callback_data=SetupScrobblingCallback(init=False, approved=False).pack()
        )
    ]])