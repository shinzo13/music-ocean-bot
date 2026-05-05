from aiogram_i18n.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_i18n import LazyProxy

from app.bot.constants import BACK_EMOJI_ID
from app.bot.callbacks.mailing_callback import MailingCallback
from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath


def mailing_message_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[ # noqa
        InlineKeyboardButton(
            text=LazyProxy('btn-back'),
            callback_data=MainMenuCallback(path=MainMenuPath.ADMIN_PANEL).pack(),
            icon_custom_emoji_id=BACK_EMOJI_ID
        )
    ]])

def mailing_approve_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[ # noqa
        [InlineKeyboardButton(
            text=LazyProxy('btn-mailing-send'),
            callback_data=MailingCallback(approved=True).pack(),
        )],
        [InlineKeyboardButton(
            text=LazyProxy('btn-cancel'),
            callback_data=MailingCallback(approved=False).pack(),
        )]
    ])