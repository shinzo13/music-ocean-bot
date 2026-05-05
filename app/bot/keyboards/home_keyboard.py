from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath
from app.bot.constants import GUIDE_EMOJI_ID, PROFILE_EMOJI_ID, SETTINGS_EMOJI_ID, PANEL_EMOJI_ID


def home_keyboard(admin: bool):
    keyboard = [
        [InlineKeyboardButton(
            text=LazyProxy('btn-how-to-use'),
            callback_data=MainMenuCallback(path=MainMenuPath.GUIDE).pack(),
            icon_custom_emoji_id=GUIDE_EMOJI_ID
        )],
        [
            InlineKeyboardButton(
                text=LazyProxy('btn-profile'),
                callback_data=MainMenuCallback(path=MainMenuPath.PROFILE).pack(),
                icon_custom_emoji_id=PROFILE_EMOJI_ID
            ),
            InlineKeyboardButton(
                text=LazyProxy('btn-settings'),
                callback_data=MainMenuCallback(path=MainMenuPath.SETTINGS).pack(),
                icon_custom_emoji_id=SETTINGS_EMOJI_ID
            )
        ]
    ]
    if admin:
        keyboard.append([InlineKeyboardButton(
            text=LazyProxy('btn-admin-panel'),
            callback_data=MainMenuCallback(path=MainMenuPath.ADMIN_PANEL).pack(),
            icon_custom_emoji_id=PANEL_EMOJI_ID
        )])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)  # noqa
