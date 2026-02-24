from typing import Optional

from pydantic import BaseModel


class Artist(BaseModel):
    id: int | str
    name: str
    photo_url: str  # not sure
    listeners: Optional[int] = None
