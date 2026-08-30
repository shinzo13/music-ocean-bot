from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.callbacks.track_entity_callback import TrackEntity, TrackEntityCallback
from app.bot.constants import ALBUM_EMOJI_ID, ARTIST_EMOJI_ID
from app.modules.musicocean.enums import Engine
from app.modules.musicocean_tg.utils import engine_to_prefix


def track_info_keyboard(track_id: int | str, engine: Engine) -> InlineKeyboardMarkup:
    def button(entity: TrackEntity, text: str, emoji_id: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=LazyProxy(text),
            callback_data=TrackEntityCallback(
                engine_prefix=engine_to_prefix(engine),
                entity=entity,
                track_id=str(track_id)
            ).pack(),
            icon_custom_emoji_id=emoji_id
        )

    return InlineKeyboardMarkup(inline_keyboard=[  # noqa
        [button(TrackEntity.ALBUM, 'btn-album', ALBUM_EMOJI_ID)],
        [button(TrackEntity.ARTIST, 'btn-artist', ARTIST_EMOJI_ID)]
    ])
