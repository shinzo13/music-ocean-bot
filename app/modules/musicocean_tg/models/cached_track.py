from pydantic import BaseModel

class CachedTrack(BaseModel):
    track_id: int | str
    file_id: str