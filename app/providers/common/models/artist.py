from pydantic import BaseModel

class Artist(BaseModel):
    id: int
    name: str
    photo_url: str # not sure
    listeners: int # not sure!!