from app.modules.musicocean.engines.soundcloud.utils import format_cover_url
from app.modules.musicocean.models import Playlist

class SoundCloudPlaylist(Playlist):

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            title=data["title"],
            cover_url=format_cover_url(data["artwork_url"]),
            track_count=data["track_count"]
        )