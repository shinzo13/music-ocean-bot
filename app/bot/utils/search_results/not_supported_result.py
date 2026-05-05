from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineQueryResultArticle, InputTextMessageContent


def not_supported_result(feature: str):
    return [InlineQueryResultArticle(
        id="not_supported",
        title=LazyProxy('not-supported-title', feature=feature),
        description=LazyProxy('not-supported-description'),
        input_message_content=InputTextMessageContent(
            message_text="meow"
        )
    )]
