from typing import Optional

from pydantic import BaseModel


class TrackPreview(BaseModel):
    id: int
    title: str
    artist_name: str
    # TODO album_title: str
    cover_url: Optional[str]
    preview_url: Optional[str]
