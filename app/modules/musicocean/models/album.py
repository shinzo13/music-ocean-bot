from pydantic import BaseModel

from app.modules.musicocean.models import Artist


class Album(BaseModel):
    id: int
    title: str
    artist: Artist
    cover_url: str # not sure