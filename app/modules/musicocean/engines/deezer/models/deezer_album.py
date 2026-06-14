from app.modules.musicocean.engines.deezer.constants import COVER_URL
from app.modules.musicocean.engines.shared.models import BaseAlbum


class DeezerAlbum(BaseAlbum):

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=int(data['id']),
            title=data['title'],
            artist_name=data['artist']['name'],
            cover_url=data['cover_xl'] or COVER_URL.format(album_id=data['id']),
        )
