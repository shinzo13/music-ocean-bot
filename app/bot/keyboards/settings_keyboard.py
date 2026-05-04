from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.constants import ENGINE_EMOJI_ID, APPEARANCE_EMOJI_ID, BACK_EMOJI_ID, MUSIC_EMOJI_ID
from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath
from app.bot.callbacks.settings_callback import SettingsCallback, SettingsPath


def settings_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Music engine",
            callback_data=SettingsCallback(path=SettingsPath.ENGINE).pack(),
            icon_custom_emoji_id=ENGINE_EMOJI_ID
        )],
        [InlineKeyboardButton(
            text="Spotify scrobbling",
            callback_data=SettingsCallback(path=SettingsPath.SCROBBLING).pack(),
            icon_custom_emoji_id=MUSIC_EMOJI_ID
        )],
        [InlineKeyboardButton(
            text="Track previews",
            callback_data=SettingsCallback(path=SettingsPath.PREVIEWS).pack(),
            icon_custom_emoji_id=APPEARANCE_EMOJI_ID
        )],
        [InlineKeyboardButton(
            text="Back",
            callback_data=MainMenuCallback(path=MainMenuPath.SELF).pack(),
            icon_custom_emoji_id=BACK_EMOJI_ID
        )]
    ])