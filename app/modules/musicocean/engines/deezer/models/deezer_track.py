from typing import Optional

from app.modules.musicocean.engines.deezer.constants import COVER_URL
from app.modules.musicocean.engines.shared.models import BaseTrack


class DeezerTrack(BaseTrack):
    track_token: Optional[str] = None
    duration: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=int(data["SNG_ID"]),
            title=data["SNG_TITLE"],
            cover_url=COVER_URL.format(album_id=data['ALB_ID']),
            track_token=data["TRACK_TOKEN"],
            artist_name=", ".join(data.get("SNG_CONTRIBUTORS", {}).get("main_artist") or [data.get("ART_NAME", "Unknown")]),
            duration=data["DURATION"]
        )
