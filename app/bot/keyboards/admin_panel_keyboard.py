from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.constants import DATABASE_EMOJI_ID, BACK_EMOJI_ID
from app.bot.callbacks.admin_panel_callback import AdminPanelCallback, AdminPanelPath
from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath


def admin_panel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Export users",
            callback_data=AdminPanelCallback(path=AdminPanelPath.EXPORT_USERS).pack(),
            icon_custom_emoji_id=DATABASE_EMOJI_ID
        )],
        [InlineKeyboardButton(
            text="Mailing",
            callback_data=AdminPanelCallback(path=AdminPanelPath.EXPORT_USERS).pack(),
        )],
        # TODO promote/ban user button
        [InlineKeyboardButton(
            text="Back",
            callback_data=MainMenuCallback(path=MainMenuPath.SELF).pack(),
            icon_custom_emoji_id=BACK_EMOJI_ID
        )]
    ])