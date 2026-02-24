from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.constants import GUIDE_EMOJI_ID, PROFILE_EMOJI_ID, SETTINGS_EMOJI_ID, PANEL_EMOJI_ID


def home_keyboard(admin: bool):
    keyboard = [
        [InlineKeyboardButton(
            text="How to use?",
            callback_data="usage_guide",
            icon_custom_emoji_id=GUIDE_EMOJI_ID
        )],
        [
            InlineKeyboardButton(
                text="Profile",
                callback_data="profile",
                icon_custom_emoji_id=PROFILE_EMOJI_ID
            ),
            InlineKeyboardButton(
                text="Settings",
                callback_data="settings",
                icon_custom_emoji_id=SETTINGS_EMOJI_ID
            )
        ]
    ]
    if admin:
        keyboard.append([InlineKeyboardButton(
            text="Admin panel",
            callback_data="admin",
            icon_custom_emoji_id=PANEL_EMOJI_ID
        )])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)