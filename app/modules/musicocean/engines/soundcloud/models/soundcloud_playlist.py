from app.modules.musicocean.engines.shared.models import BasePlaylist
from app.modules.musicocean.engines.soundcloud.utils import format_cover_url


class SoundCloudPlaylist(BasePlaylist):

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            title=data["title"],
            cover_url=format_cover_url(data["artwork_url"]),
            track_count=data["track_count"]
        )
