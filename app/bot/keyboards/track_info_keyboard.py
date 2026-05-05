from aiogram_i18n.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_i18n import LazyProxy

from app.bot.constants import ALBUM_EMOJI_ID, ARTIST_EMOJI_ID
from app.modules.musicocean.enums import Engine
from app.modules.musicocean_tg.utils import engine_to_prefix


def track_info_keyboard(track_id: int, engine: Engine) -> InlineKeyboardMarkup:
    full_id = f"{engine_to_prefix(engine)}-{track_id}"
    return InlineKeyboardMarkup(inline_keyboard=[ # noqa
        [InlineKeyboardButton(
            text=LazyProxy('btn-album'),
            callback_data=f"{full_id}-album",
            icon_custom_emoji_id=ALBUM_EMOJI_ID
        )],
        [InlineKeyboardButton(
            text=LazyProxy('btn-artist'),
            callback_data=f"{full_id}-artist",
            icon_custom_emoji_id=ARTIST_EMOJI_ID
        )]
    ])