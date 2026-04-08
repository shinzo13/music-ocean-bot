from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.constants import SPOTIFY_EMOJI_ID
from app.bot.utils.get_lastfm_auth_url import get_lastfm_auth_url


def scrobbling_setup_keyboard(bot_username: str):
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="Setup scrobbling",
            url=f"https://t.me/{bot_username}?start=setup_scrobbling",
            icon_custom_emoji_id=SPOTIFY_EMOJI_ID
        )
    ]])

def oauth_scrobbling_keyboard(user_id: int):
    url = get_lastfm_auth_url(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="Log in to Spotify",
            url=url,
            icon_custom_emoji_id=SPOTIFY_EMOJI_ID
        )
    ]])

