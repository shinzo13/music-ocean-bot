from typing import Optional

from pydantic import BaseModel


class BaseTrackPreview(BaseModel):
    id: int | str
    title: str
    artist_name: str
    # TODO album_title: str
    cover_url: Optional[str]
    preview_url: Optional[str] = None
    # Where the track came from, when the engine says so: youtube has neither,
    # soundcloud has no album. None means "cannot be looked up", which the
    # album/artist buttons report rather than fail on.
    album_id: Optional[int | str] = None
    artist_id: Optional[int | str] = None
