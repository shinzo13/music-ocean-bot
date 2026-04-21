from pydantic import BaseModel


class BaseAlbum(BaseModel):
    id: int | str
    title: str
    artist_name: str
    cover_url: str  # not sure
