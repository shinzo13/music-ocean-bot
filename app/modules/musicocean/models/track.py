from typing import Optional

from pydantic import BaseModel


class Track(BaseModel):
    """
    Basic Track model. Contains all the information needed to properly download a track.
    """

    id: int
    title: str
    artist_name: str
    # TODO album_title: str
    cover_url: str

    preview_url: Optional[str] = None
    track_token: Optional[str] = None
    duration: Optional[int] = None
    content: Optional[bytes] = None
    cover: Optional[bytes] = None