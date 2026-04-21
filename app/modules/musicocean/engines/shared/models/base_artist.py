from typing import Optional

from pydantic import BaseModel


class BaseArtist(BaseModel):
    id: int | str
    name: str
    photo_url: str  # not sure
    listeners: Optional[int] = None
