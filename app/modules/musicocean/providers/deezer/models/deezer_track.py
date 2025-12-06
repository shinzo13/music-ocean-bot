from typing import Optional

from app.modules.musicocean.models import Track
from app.modules.musicocean.providers.deezer.constants import COVER_URL


class DeezerTrack(Track):
    track_token: Optional[str] = None
    duration: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=int(data["SNG_ID"]),
            title=data["SNG_TITLE"],
            cover_url=COVER_URL.format(album_id=data['ALB_ID']),
            track_token=data["TRACK_TOKEN"],
            artist_name=", ".join(data["SNG_CONTRIBUTORS"]["main_artist"]),
            duration=data["DURATION"]
        )