from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.callbacks.default_engine_callback import DefaultEngineCallback
from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath
from app.bot.constants import SOUNDCLOUD_EMOJI_ID, DEEZER_EMOJI_ID, BACK_EMOJI_ID, YOUTUBE_EMOJI_ID, SPOTIFY_EMOJI_ID, \
    YANDEX_EMOJI_ID
from app.bot.utils.selected_option import option_selection
from app.config.settings import settings
from app.modules.musicocean.enums import Engine
from app.config.log import get_logger

logger = get_logger(__name__)

ENGINE_OPTIONS = [
    (Engine.DEEZER, "Deezer", 'dz', DEEZER_EMOJI_ID),
    (Engine.SOUNDCLOUD, "SoundCloud", 'sc', SOUNDCLOUD_EMOJI_ID),
    (Engine.YOUTUBE, "YTMusic", 'yt', YOUTUBE_EMOJI_ID),
    (Engine.SPOTIFY, "Spotify", 'sp', SPOTIFY_EMOJI_ID),
    (Engine.YANDEX, "Yandex Music", 'ya', YANDEX_EMOJI_ID),
]


def engines_keyboard(engine: Engine):
    logger.debug(f"engines_keyboard: {engine}")
    keyboard = [
        [InlineKeyboardButton(
            text=option_selection(label, engine == option),
            callback_data=DefaultEngineCallback(engine_prefix=prefix).pack(),
            icon_custom_emoji_id=emoji_id,
            style='success' if engine == option else None
        )]
        for option, label, prefix, emoji_id in ENGINE_OPTIONS
        if settings.engines.is_enabled(option)
    ]
    keyboard.append([InlineKeyboardButton(
        text=LazyProxy('btn-back'),
        callback_data=MainMenuCallback(path=MainMenuPath.SETTINGS).pack(),
        icon_custom_emoji_id=BACK_EMOJI_ID
    )])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)  # noqa
