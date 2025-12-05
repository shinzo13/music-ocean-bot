from pydantic import BaseModel


class Album(BaseModel):
    id: int
    title: str
    artist_name: str
    cover_url: str # not sure