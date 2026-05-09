from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath
from app.bot.callbacks.setup_scrobbling_callback import SetupScrobblingCallback
from app.bot.constants import BACK_EMOJI_ID


def scrobbling_setup_keyboard(again: bool = False):
    return InlineKeyboardMarkup(inline_keyboard=[  # noqa
        [InlineKeyboardButton(
            text=LazyProxy(f'btn-setup-scrobbling{'-again' if again else ''}'),
            callback_data=SetupScrobblingCallback(init=True, approved=False).pack()
            # TODO lastfm icon
        )],
        [InlineKeyboardButton(
            text=LazyProxy('btn-back'),
            callback_data=MainMenuCallback(path=MainMenuPath.SETTINGS).pack(),
            icon_custom_emoji_id=BACK_EMOJI_ID
        )]
    ])
