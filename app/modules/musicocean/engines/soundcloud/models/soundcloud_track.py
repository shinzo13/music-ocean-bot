from app.modules.musicocean.engines.soundcloud.utils import format_cover_url
from app.modules.musicocean.models import Track


class SoundCloudTrack(Track):

        @classmethod
        def from_dict(cls, data: dict):
            return cls(
                id=int(data["id"]),
                title=data["title"],
                artist_name=data['user']['username'],
                cover_url=format_cover_url(data["artwork_url"]),
                duration=int(data["duration"]/1000),
            )