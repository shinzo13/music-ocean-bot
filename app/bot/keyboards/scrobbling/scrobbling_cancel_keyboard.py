from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.constants import SPOTIFY_EMOJI_ID, BACK_EMOJI_ID
from app.bot.callbacks.settings_callback import SettingsCallback, SettingsPath


def scrobbling_cancel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="Cancel",
            callback_data=SettingsCallback(path=SettingsPath.SCROBBLING).pack(),
            icon_custom_emoji_id=BACK_EMOJI_ID
        )
    ]])