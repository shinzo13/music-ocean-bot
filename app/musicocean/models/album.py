from pydantic import BaseModel

from app.musicocean.providers.deezer.models.deezer_artist import Artist


class Album(BaseModel):
    id: int
    title: str
    artist: Artist
    cover_url: str # not sure