from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup

from app.bot.constants import SPOTIFY_LOGO_URL, SPOTIFY_BANNER_URL
from app.bot.keyboards.scrobbling import scrobbling_setup_keyboard


def setup_scrobbling_result(bot_username: str):
    return [InlineQueryResultArticle(
        id="setup_scrobbling",
        title="Spotify scrobbling",
        description="Setup scrobbling to download tracks you are listening now to!",
        input_message_content=InputTextMessageContent(
            message_text=f"<b>Spotify scrobbling!!</b>\n\nLog in into your Spotify account and get ability to quickly download tracks from your player.<a href='{SPOTIFY_BANNER_URL}'>︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎</a>"  # TODO
        ),
        reply_markup=scrobbling_setup_keyboard(bot_username),
        thumbnail_url=SPOTIFY_LOGO_URL,
        thumbnail_width=565,
        thumbnail_height=565
    )]
