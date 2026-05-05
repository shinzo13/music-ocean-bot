from aiogram_i18n import LazyProxy, I18nContext
from aiogram_i18n.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath
from app.bot.callbacks.track_previews_callback import TrackPreviewsCallback
from app.bot.constants import BACK_EMOJI_ID, COVER_EMOJI_ID, MUSIC_EMOJI_ID
from app.bot.utils.selected_option import option_selection


# cant do LazyProxy as it renders after the option_selection() call
def track_preview_keyboard(i18n: I18nContext, show_covers: bool) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[  # noqa
        [InlineKeyboardButton(
            text=option_selection(
                i18n.get('btn-show-covers'),
                show_covers
            ),
            callback_data=TrackPreviewsCallback(show_covers=True).pack(),
            icon_custom_emoji_id=COVER_EMOJI_ID
        )],
        [InlineKeyboardButton(
            text=option_selection(
                i18n.get('btn-show-mp3-previews'),
                not show_covers
            ),
            callback_data=TrackPreviewsCallback(show_covers=False).pack(),
            icon_custom_emoji_id=MUSIC_EMOJI_ID
        )],
        [InlineKeyboardButton(
            text=LazyProxy('btn-back'),
            callback_data=MainMenuCallback(path=MainMenuPath.SETTINGS).pack(),
            icon_custom_emoji_id=BACK_EMOJI_ID
        )]
    ])
