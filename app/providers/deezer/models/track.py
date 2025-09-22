from pydantic import BaseModel

from app.providers.deezer.models.album import Album
from app.providers.deezer.models.artist import Artist


class DeezerTrack(BaseModel):
    id: int
    title: str
    artist: Artist
    album: Album
