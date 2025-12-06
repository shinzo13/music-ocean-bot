from aiogram.types import InlineQueryResultArticle, InputTextMessageContent


def usage_guide_result():
    return [InlineQueryResultArticle(
        id="usage_guide",
        title="How to use advanced search?",
        description="Click here to see usage guide.",
        input_message_content=InputTextMessageContent(
            message_text=f"<b>How to use advanced search?</b>\n\ni dont know" # TODO
        )
    )]
