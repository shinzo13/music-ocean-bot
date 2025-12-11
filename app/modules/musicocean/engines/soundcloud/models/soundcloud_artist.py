from app.modules.musicocean.engines.soundcloud.utils import format_cover_url
from app.modules.musicocean.models import Artist


class SoundCloudArtist(Artist):

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            name=data["username"],
            photo_url=format_cover_url(data["avatar_url"]),  # TODO rename method
            listeners=data["followers_count"],
        )
