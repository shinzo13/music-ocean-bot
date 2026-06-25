from pydantic import BaseModel


class CachedTrack(BaseModel):
    track_id: int | str
    file_id: str
    file_unique_id: str | None = None
    artist_name: str | None = None
    title: str | None = None
