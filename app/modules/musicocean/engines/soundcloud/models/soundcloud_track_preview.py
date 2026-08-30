from app.modules.musicocean.engines.shared.models import BaseTrackPreview
from app.modules.musicocean.engines.soundcloud.utils import format_cover_url


class SoundCloudTrackPreview(BaseTrackPreview):

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=int(data["id"]),
            title=data["title"],
            artist_name=data['user']['username'],
            cover_url=format_cover_url(data["artwork_url"]),
            preview_url=None,
            # soundcloud has uploaders, not albums: a track belongs to a user
            # and optionally to playlists, so only the artist can be resolved
            artist_id=data['user'].get('id')
        )
