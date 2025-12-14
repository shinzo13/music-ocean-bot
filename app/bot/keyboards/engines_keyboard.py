from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.modules.musicocean.enums import Engine

def engines_keyboard(engine: Engine):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"{'✨ ' if engine==Engine.DEEZER else ''}Deezer",
            callback_data="set_engine_dz"
        )],
        [InlineKeyboardButton(
            text=f"{'✨ ' if engine==Engine.SOUNDCLOUD else ''}SoundCloud",
            callback_data="set_engine_sc"
        )],
#        [InlineKeyboardButton(text="YouTube", callback_data="set_engine_dz")],
#        [InlineKeyboardButton(text="Spotify", callback_data="set_engine_dz")]
        [InlineKeyboardButton(text="⬅️ Back", callback_data="settings")]
    ])