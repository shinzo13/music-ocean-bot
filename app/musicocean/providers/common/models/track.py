from pydantic import BaseModel


class Track(BaseModel):
    id: int
    title: str
    artist_name: str
    # TODO album_title: str
    cover_url: str
