from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath
from app.bot.callbacks.setup_scrobbling_callback import SetupScrobblingCallback
from app.bot.constants import SPOTIFY_EMOJI_ID, BACK_EMOJI_ID


def scrobbling_setup_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="Setup scrobbling",
            callback_data=SetupScrobblingCallback(init=True, approved=False).pack(),
            icon_custom_emoji_id=SPOTIFY_EMOJI_ID
        ),
        InlineKeyboardButton(
            text="Back",
            callback_data=MainMenuCallback(path=MainMenuPath.SETTINGS).pack(),
            icon_custom_emoji_id=BACK_EMOJI_ID
        )
    ]])