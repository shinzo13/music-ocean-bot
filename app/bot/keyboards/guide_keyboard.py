from aiogram_i18n.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_i18n import LazyProxy

from app.bot.constants import BACK_EMOJI_ID
from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath


# TODO back_home_kb if here would be no more content
def guide_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[ # noqa
        InlineKeyboardButton(
            text=LazyProxy('btn-back'),
            callback_data=MainMenuCallback(path=MainMenuPath.SELF).pack(),
            icon_custom_emoji_id=BACK_EMOJI_ID
        )
    ]])