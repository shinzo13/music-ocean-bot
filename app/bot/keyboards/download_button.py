from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.constants import DOWNLOAD_EMOJI_ID, LOADING_EMOJI_ID


CALLBACK_DATA_LIMIT = 64


def download_keyboard(track_ref: str) -> InlineKeyboardMarkup | None:
    """The button carries the same id as the inline result, so a press does the
    same work as the chosen-result update. Telegram delivers that update only
    sometimes — and never at all for some senders — so the press is what makes
    a download reliable rather than a nicety."""
    # telegram rejects the whole inline answer over the callback data limit —
    # an exotic id costs its button, not the entire result list
    if len(track_ref.encode()) > CALLBACK_DATA_LIMIT:
        return None
    return InlineKeyboardMarkup(inline_keyboard=[[  # noqa
        InlineKeyboardButton(
            text=LazyProxy('btn-click-to-download'),
            callback_data=track_ref,
            icon_custom_emoji_id=DOWNLOAD_EMOJI_ID
        )
    ]])


def downloading_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[  # noqa
        InlineKeyboardButton(
            text=LazyProxy('btn-downloading'),
            callback_data="downloading",
            icon_custom_emoji_id=LOADING_EMOJI_ID
        )
    ]])
