from pydantic import BaseModel

from app.providers.common.models import Album
from app.providers.common.models import Artist


class Track(BaseModel):
    id: int
    title: str
    artist_name: str
    # TODO album_title: str
    cover_url: str
