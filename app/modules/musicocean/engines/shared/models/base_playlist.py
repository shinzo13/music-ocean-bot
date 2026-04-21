from pydantic import BaseModel


class BasePlaylist(BaseModel):
    id: int | str
    title: str
    cover_url: str
    track_count: int
