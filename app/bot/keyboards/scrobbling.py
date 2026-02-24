from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.constants import SPOTIFY_EMOJI_ID
from app.modules.musicocean.engines.spotify.constants import SPOTIFY_SCROBBLE_URL


def scrobbling_setup_keyboard(bot_username: str):
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="Setup scrobbling",
            url=f"https://t.me/{bot_username}?start=setup_scrobbling",
            icon_custom_emoji_id=SPOTIFY_EMOJI_ID
        )
    ]])

def oauth_scrobbling_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="Log in to Spotify",
            url=SPOTIFY_SCROBBLE_URL,
            icon_custom_emoji_id=SPOTIFY_EMOJI_ID
        )
    ]])

