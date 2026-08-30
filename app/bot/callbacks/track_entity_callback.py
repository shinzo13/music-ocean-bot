from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


class TrackEntity(StrEnum):
    ALBUM = "al"
    ARTIST = "ar"


class TrackEntityCallback(CallbackData, prefix="tent"):
    """The album or artist a track belongs to, asked for from the track card."""
    engine_prefix: str
    entity: TrackEntity
    track_id: str
