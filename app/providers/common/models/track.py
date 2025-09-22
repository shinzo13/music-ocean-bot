from pydantic import BaseModel

from app.providers.common.models import Album
from app.providers.common.models import Artist


class Track(BaseModel):
    id: int
    title: str
    artist: Artist
    album: Album
