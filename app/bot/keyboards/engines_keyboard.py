from aiogram_i18n.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_i18n import LazyProxy

from app.bot.constants import SOUNDCLOUD_EMOJI_ID, DEEZER_EMOJI_ID, BACK_EMOJI_ID, YOUTUBE_EMOJI_ID, SPOTIFY_EMOJI_ID
from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath
from app.bot.callbacks.default_engine_callback import DefaultEngineCallback
from app.bot.utils.selected_option import option_selection
from app.modules.musicocean.enums import Engine

def engines_keyboard(engine: Engine):
    return InlineKeyboardMarkup(inline_keyboard=[ # noqa
        [InlineKeyboardButton(
            text=option_selection("Deezer", engine==Engine.DEEZER),
            callback_data=DefaultEngineCallback(engine_prefix='dz').pack(),
            icon_custom_emoji_id=DEEZER_EMOJI_ID,
        )],
        [InlineKeyboardButton(
            text=option_selection("SoundCloud", engine==Engine.SOUNDCLOUD),
            callback_data=DefaultEngineCallback(engine_prefix='sc').pack(),
            icon_custom_emoji_id=SOUNDCLOUD_EMOJI_ID,
        )],
        [InlineKeyboardButton(
            text=option_selection("YTMusic", engine == Engine.YOUTUBE),
            callback_data=DefaultEngineCallback(engine_prefix='yt').pack(),
            icon_custom_emoji_id=YOUTUBE_EMOJI_ID,
        )],
        [InlineKeyboardButton(
            text=option_selection("Spotify", engine == Engine.SPOTIFY),
            callback_data=DefaultEngineCallback(engine_prefix='sp').pack(),
            icon_custom_emoji_id=SPOTIFY_EMOJI_ID,
        )],
        [InlineKeyboardButton(
            text=LazyProxy('btn-back'),
            callback_data=MainMenuCallback(path=MainMenuPath.SETTINGS).pack(),
            icon_custom_emoji_id=BACK_EMOJI_ID,
        )]
    ])