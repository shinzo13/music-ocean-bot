from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardMarkup, InlineKeyboardButton


def scrobbling_inline_setup_keyboard(bot_username: str):
    return InlineKeyboardMarkup(inline_keyboard=[[  # noqa
        InlineKeyboardButton(
            text=LazyProxy(f'btn-setup-scrobbling'),
            url=f"https://t.me/{bot_username}?start=setup_scrobbling"
        )
    ]])
