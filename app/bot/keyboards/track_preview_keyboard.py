from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.constants import BACK_EMOJI_ID, COVER_EMOJI_ID, MUSIC_EMOJI_ID
from app.bot.callbacks.track_previews_callback import TrackPreviewsCallback
from app.bot.utils.selected_option import option_selection


def track_preview_keyboard(show_covers: bool) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=option_selection("Show covers", show_covers),
            callback_data=TrackPreviewsCallback(show_covers=True).pack(),
            icon_custom_emoji_id=COVER_EMOJI_ID
        )],
        [InlineKeyboardButton(
            text=option_selection("Show MP3 previews", not show_covers),
            callback_data=TrackPreviewsCallback(show_covers=False).pack(),
            icon_custom_emoji_id=MUSIC_EMOJI_ID
        )],
        [InlineKeyboardButton(
            text="Back",
            callback_data="settings",
            icon_custom_emoji_id=BACK_EMOJI_ID
        )]
    ])