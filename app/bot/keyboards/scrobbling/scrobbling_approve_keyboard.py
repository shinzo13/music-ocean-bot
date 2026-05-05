from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.callbacks.setup_scrobbling_callback import SetupScrobblingCallback


def scrobbling_approve_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[  # noqa
        InlineKeyboardButton(
            text=LazyProxy('btn-yes'),
            callback_data=SetupScrobblingCallback(init=False, approved=True).pack()
        ),
        InlineKeyboardButton(
            text=LazyProxy('btn-no'),
            callback_data=SetupScrobblingCallback(init=False, approved=False).pack()
        )
    ]])
