from pydantic import BaseModel

from app.modules.musicocean.enums.engine import Engine


class CachedTrack(BaseModel):
    track_id: int | str
    file_id: str
    file_unique_id: str | None = None
    artist_name: str | None = None
    title: str | None = None
    # for spotify: the engine the audio was actually pulled from
    source_engine: Engine | None = None
    source_id: int | str | None = None
