from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.constants import DATABASE_EMOJI_ID, BACK_EMOJI_ID


def admin_panel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Export users",
            callback_data="users",
            icon_custom_emoji_id=DATABASE_EMOJI_ID
        )],
        # TODO promote/ban user button
        [InlineKeyboardButton(
            text="Back",
            callback_data="main_menu",
            icon_custom_emoji_id=BACK_EMOJI_ID
        )]
    ])