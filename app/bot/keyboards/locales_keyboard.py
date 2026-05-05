from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.callbacks.locales_callback import LocalesCallback
from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath
from app.bot.constants import BACK_EMOJI_ID
from app.bot.utils.selected_option import option_selection


def locales_keyboard(current: str):
    return InlineKeyboardMarkup(inline_keyboard=[  # noqa
        [InlineKeyboardButton(
            text=option_selection('🇬🇧 English', current == 'en'),
            callback_data=LocalesCallback(code='en').pack()
        )],
        [InlineKeyboardButton(
            text=option_selection('🇵🇱 Polski', current == 'pl'),
            callback_data=LocalesCallback(code='pl').pack()
        )],
        [InlineKeyboardButton(
            text=option_selection('🇺🇦 Українська', current == 'uk'),
            callback_data=LocalesCallback(code='uk').pack()
        )],
        [InlineKeyboardButton(
            text=option_selection('🇷🇺 Русский', current == 'ru'),
            callback_data=LocalesCallback(code='ru').pack()
        )],
        [InlineKeyboardButton(
            text=LazyProxy('btn-back'),
            callback_data=MainMenuCallback(path=MainMenuPath.SETTINGS).pack(),
            icon_custom_emoji_id=BACK_EMOJI_ID
        )]
    ])
