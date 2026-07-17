from typing import Optional

from pydantic import BaseModel


class BasePlaylist(BaseModel):
    id: int | str
    title: str
    cover_url: Optional[str] = None
    track_count: int
