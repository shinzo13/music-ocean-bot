from typing import Optional

from app.musicocean.providers.common.models import Track
from app.musicocean.providers.deezer.constants import COVER_URL

class DeezerTrack(Track):
    preview_url: Optional[str] = None   # API
    track_token: Optional[str] = None   # Client
    duration: Optional[int] = None      # Client

    @classmethod
    def from_api(cls, data: dict):
        return cls(
            id=int(data["id"]),
            title=data["title"],
            artist_name=data['artist']['name'],
            cover_url=COVER_URL.format(image_id=data['md5_image']),
            preview_url=data['preview']
        )

    @classmethod
    def from_client(cls, data: dict):
        return cls(
            id=int(data["SNG_ID"]),
            title=data["SNG_TITLE"],
            cover_url=COVER_URL.format(data['ALB_PICTURE']),
            track_token=data["TRACK_TOKEN"],
            artist_name=", ".join(data["SNG_CONTRIBUTORS"]["main_artist"]),
            duration=data["DURATION"]
        )