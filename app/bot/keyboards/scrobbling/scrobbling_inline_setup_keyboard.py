from aiogram_i18n.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_i18n import LazyProxy

from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath
from app.bot.callbacks.setup_scrobbling_callback import SetupScrobblingCallback
from app.bot.constants import SPOTIFY_EMOJI_ID, BACK_EMOJI_ID


def scrobbling_inline_setup_keyboard(bot_username: str):
    return InlineKeyboardMarkup(inline_keyboard=[[ # noqa
        InlineKeyboardButton(
            text=LazyProxy(f'btn-setup-scrobbling'),
            url=f"https://t.me/{bot_username}?start=setup_scrobbling"
        )
    ]])