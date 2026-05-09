from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineQueryResultArticle, InputTextMessageContent


def usage_guide_result():
    return [InlineQueryResultArticle(
        id="usage_guide",
        title=LazyProxy('usage-guide-title'),
        description=LazyProxy('usage-guide-description'),
        input_message_content=InputTextMessageContent(
            message_text=LazyProxy('usage-guide-message')
        )
    )]
