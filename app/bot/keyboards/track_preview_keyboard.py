from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def track_preview_keyboard(show_covers: bool) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{'✨ ' if show_covers else ''}Show covers", callback_data="set_previews_covers")],
        [InlineKeyboardButton(text=f"{'' if show_covers else '✨ '}Show MP3 previews (if available)", callback_data="set_previews_mp3")],
        [InlineKeyboardButton(text="⬅️ Back", callback_data="settings")]
    ])