from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.callbacks.admin_panel_callback import AdminPanelCallback, AdminPanelPath
from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath
from app.bot.constants import DATABASE_EMOJI_ID, BACK_EMOJI_ID, MAILING_EMOJI_ID


def admin_panel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[  # noqa
        [InlineKeyboardButton(
            text=LazyProxy('btn-export-users'),
            callback_data=AdminPanelCallback(path=AdminPanelPath.EXPORT_USERS).pack(),
            icon_custom_emoji_id=DATABASE_EMOJI_ID
        )],
        [InlineKeyboardButton(
            text=LazyProxy('btn-mailing'),
            callback_data=AdminPanelCallback(path=AdminPanelPath.MAILING).pack(),
            icon_custom_emoji_id=MAILING_EMOJI_ID
        )],
        # TODO promote/ban user button
        [InlineKeyboardButton(
            text=LazyProxy('btn-back'),
            callback_data=MainMenuCallback(path=MainMenuPath.SELF).pack(),
            icon_custom_emoji_id=BACK_EMOJI_ID
        )]
    ])
