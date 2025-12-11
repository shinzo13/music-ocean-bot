from app.modules.musicocean.engines.deezer.constants import COVER_URL
from app.modules.musicocean.models import TrackPreview


class DeezerTrackPreview(TrackPreview):

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=int(data["id"]),
            title=data["title"],
            artist_name=data['artist']['name'],
            cover_url=COVER_URL.format(album_id=data['album']['id']),
            preview_url=data['preview']
        )
