from typing import Optional

from app.modules.musicocean.models import TrackPreview
from app.modules.musicocean.providers.deezer.constants import COVER_URL


class DeezerTrackPreview(TrackPreview):

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=int(data["id"]),
            title=data["title"],
            artist_name=data['artist']['name'],
            cover_url=COVER_URL.format(image_id=data['md5_image']),
            preview_url=data['preview']
        )