from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.callbacks.settings_callback import SettingsCallback, SettingsPath
from app.bot.constants import BACK_EMOJI_ID


def scrobbling_cancel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[  # noqa
        InlineKeyboardButton(
            text=LazyProxy('btn-cancel'),
            callback_data=SettingsCallback(path=SettingsPath.SCROBBLING).pack(),
            icon_custom_emoji_id=BACK_EMOJI_ID
        )
    ]])
