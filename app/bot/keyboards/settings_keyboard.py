from aiogram_i18n.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_i18n import LazyProxy

from app.bot.constants import ENGINE_EMOJI_ID, APPEARANCE_EMOJI_ID, BACK_EMOJI_ID, MUSIC_EMOJI_ID, LOCALE_EMOJI_ID
from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath
from app.bot.callbacks.settings_callback import SettingsCallback, SettingsPath


def settings_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[ # noqa
        [InlineKeyboardButton(
            text=LazyProxy('btn-language'),
            callback_data=SettingsCallback(path=SettingsPath.LOCALE).pack(),
            icon_custom_emoji_id=LOCALE_EMOJI_ID
        )],
        [InlineKeyboardButton(
            text=LazyProxy('btn-music-engine'),
            callback_data=SettingsCallback(path=SettingsPath.ENGINE).pack(),
            icon_custom_emoji_id=ENGINE_EMOJI_ID
        )],
        [InlineKeyboardButton(
            text=LazyProxy('btn-scrobbling'),
            callback_data=SettingsCallback(path=SettingsPath.SCROBBLING).pack(),
            icon_custom_emoji_id=MUSIC_EMOJI_ID
        )],
        [InlineKeyboardButton(
            text=LazyProxy('btn-track-previews'),
            callback_data=SettingsCallback(path=SettingsPath.PREVIEWS).pack(),
            icon_custom_emoji_id=APPEARANCE_EMOJI_ID
        )],
        [InlineKeyboardButton(
            text=LazyProxy('btn-back'),
            callback_data=MainMenuCallback(path=MainMenuPath.SELF).pack(),
            icon_custom_emoji_id=BACK_EMOJI_ID
        )]
    ])