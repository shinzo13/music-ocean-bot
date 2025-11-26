from app.modules.musicocean.models import TrackPreview
from aiogram.types import InlineQueryResultAudio, InlineQueryResultDocument, InlineKeyboardMarkup, InlineKeyboardButton


def generate_inline_results(matches: list[TrackPreview]):
    # TODO db usage
    reply_markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="downloading",
            callback_data="x"
        )
    ]])

    return [
        InlineQueryResultAudio(
            id=str(track.id),
            audio_url=track.preview_url,
            title=track.title,
            performer=track.artist_name, # not sure if needed
            reply_markup=reply_markup,
        ) \
        if track.preview_url else \
        InlineQueryResultDocument(
            id=str(track.id),
            title=track.title,
            document_url=track.cover_url,
            mime_type="application/zip",
            caption=track.artist_name+"muhehe",
            reply_markup=reply_markup
        )
        for track in matches
    ]
