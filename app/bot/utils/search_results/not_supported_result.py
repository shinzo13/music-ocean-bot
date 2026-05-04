from aiogram.types import InlineQueryResultArticle, InputTextMessageContent


def not_supported_result(feature: str):
    return [InlineQueryResultArticle(
        id="not_supported",
        title=f"{feature} is not supported at the moment",
        description=":(",
        input_message_content=InputTextMessageContent(
            message_text="meow"
        )
    )]
