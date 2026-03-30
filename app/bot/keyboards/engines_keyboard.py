from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.constants import SOUNDCLOUD_EMOJI_ID, DEEZER_EMOJI_ID, BACK_EMOJI_ID, YOUTUBE_EMOJI_ID, SPOTIFY_EMOJI_ID
from app.bot.utils.selected_option import option_selection
from app.modules.musicocean.enums import Engine

def engines_keyboard(engine: Engine):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=option_selection("Deezer", engine==Engine.DEEZER),
            callback_data="set_engine_dz",
            icon_custom_emoji_id=DEEZER_EMOJI_ID,
        )],
        [InlineKeyboardButton(
            text=option_selection("SoundCloud", engine==Engine.SOUNDCLOUD),
            callback_data="set_engine_sc",
            icon_custom_emoji_id=SOUNDCLOUD_EMOJI_ID,
        )],
        [InlineKeyboardButton(
            text=option_selection("YTMusic", engine == Engine.YOUTUBE),
            callback_data="set_engine_yt",
            icon_custom_emoji_id=YOUTUBE_EMOJI_ID,
        )],
        [InlineKeyboardButton(
            text=option_selection("Spotify", engine == Engine.SPOTIFY),
            callback_data="set_engine_sp",
            icon_custom_emoji_id=SPOTIFY_EMOJI_ID,
        )],
        [InlineKeyboardButton(
            text="Back",
            callback_data="settings",
            icon_custom_emoji_id=BACK_EMOJI_ID,
        )]
    ])