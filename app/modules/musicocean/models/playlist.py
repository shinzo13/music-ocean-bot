from pydantic import BaseModel


class Playlist(BaseModel):
    id: int
    title: str
    cover_url: str
    track_count: int
