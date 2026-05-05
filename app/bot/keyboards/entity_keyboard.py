from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.constants import SEARCH_EMOJI_ID, LOCKED_EMOJI_ID, DOWNLOAD_EMOJI_ID
from app.modules.musicocean.enums import Engine
from app.modules.musicocean_tg.utils import engine_to_prefix


def entity_keyboard(
        engine: Engine,
        bot_username: str,
        entity_id: int,
        prefix: str,
        download_all: bool = True,
        download_all_available: bool = True,

) -> InlineKeyboardMarkup:
    kb = [[InlineKeyboardButton(
        text=LazyProxy('btn-search-for-track'),
        switch_inline_query_current_chat=f"{engine_to_prefix(engine)}::{prefix}::{entity_id}",
        icon_custom_emoji_id=SEARCH_EMOJI_ID
    )]]
    if download_all:
        if download_all_available:
            kb.append([InlineKeyboardButton(
                text=LazyProxy('btn-download-all'),
                url=f"https://t.me/{bot_username}?start={engine_to_prefix(engine)}_{prefix}_{entity_id}",
                icon_custom_emoji_id=DOWNLOAD_EMOJI_ID
            )])
        else:
            kb.append([InlineKeyboardButton(
                text=LazyProxy('btn-download-all'),
                callback_data="feature_not_available",
                icon_custom_emoji_id=LOCKED_EMOJI_ID
            )])
    return InlineKeyboardMarkup(inline_keyboard=kb)  # noqa
