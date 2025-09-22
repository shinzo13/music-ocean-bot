from pydantic import BaseModel

from app.providers.deezer.models.artist import Artist


class Album(BaseModel):
    id: int
    title: str
    artist: Artist
    cover_url: str # not sure