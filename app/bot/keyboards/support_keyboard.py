from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath
from app.bot.constants import BACK_EMOJI_ID, MAILING_EMOJI_ID

SUPPORT_BOT_URL = "https://t.me/koshkesupportbot"


def support_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[  # noqa
        [InlineKeyboardButton(
            text=LazyProxy('btn-write-support'),
            url=SUPPORT_BOT_URL,
            icon_custom_emoji_id=MAILING_EMOJI_ID
        )],
        [InlineKeyboardButton(
            text=LazyProxy('btn-back'),
            callback_data=MainMenuCallback(path=MainMenuPath.SELF).pack(),
            icon_custom_emoji_id=BACK_EMOJI_ID
        )]
    ])
