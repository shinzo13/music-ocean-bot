from typing import Optional

from pydantic import BaseModel


class Artist(BaseModel):
    id: int
    name: str
    photo_url: str  # not sure
    listeners: Optional[int] = None
