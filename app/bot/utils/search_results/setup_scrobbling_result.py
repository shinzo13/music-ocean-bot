from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineQueryResultArticle, InputTextMessageContent

from app.bot.constants import SPOTIFY_LOGO_URL
from app.bot.keyboards.scrobbling import scrobbling_inline_setup_keyboard


def setup_scrobbling_result(bot_username: str):
    return [InlineQueryResultArticle(
        id="setup_scrobbling",
        title=LazyProxy('setup-scrobbling-title'),
        description=LazyProxy('setup-scrobbling-description'),
        input_message_content=InputTextMessageContent(
            message_text=LazyProxy('setup-scrobbling-message')
        ),
        reply_markup=scrobbling_inline_setup_keyboard(bot_username),
        thumbnail_url=SPOTIFY_LOGO_URL,
        thumbnail_width=565,
        thumbnail_height=565
    )]
