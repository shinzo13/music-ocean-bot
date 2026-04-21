from typing import Optional

from pydantic import BaseModel


class BaseTrackPreview(BaseModel):
    id: int | str
    title: str
    artist_name: str
    # TODO album_title: str
    cover_url: Optional[str]
    preview_url: Optional[str] = None
