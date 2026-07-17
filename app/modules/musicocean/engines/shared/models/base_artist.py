from typing import Optional

from pydantic import BaseModel


class BaseArtist(BaseModel):
    id: int | str
    name: str
    photo_url: Optional[str] = None
    listeners: Optional[int] = None
