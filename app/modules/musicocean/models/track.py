from typing import Optional

from pydantic import BaseModel


# TODO!! use Track only as MO-ready class, delete in-engine fields

class Track(BaseModel):
    """
    Basic Track model. Contains all the information needed to properly download a track.
    """

    # Necessary
    id: int
    title: str
    artist_name: str
    # TODO album_title: str
    cover_url: Optional[str]

    # Common
    duration: Optional[int] = None
    content: Optional[bytes] = None
    cover: Optional[bytes] = None

    # Deezer
    preview_url: Optional[str] = None
    track_token: Optional[str] = None