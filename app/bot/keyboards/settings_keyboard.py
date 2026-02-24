from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.constants import ENGINE_EMOJI_ID, APPEARANCE_EMOJI_ID, BACK_EMOJI_ID


def settings_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Music engine",
            callback_data="default_engine",
            icon_custom_emoji_id=ENGINE_EMOJI_ID
        )],
        [InlineKeyboardButton(
            text="Track previews",
            callback_data="track_preview_appearance",
            icon_custom_emoji_id=APPEARANCE_EMOJI_ID
        )],
        [InlineKeyboardButton(
            text="Back",
            callback_data="main_menu",
            icon_custom_emoji_id=BACK_EMOJI_ID
        )]
    ])