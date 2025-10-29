from app.musicocean.providers.common.models import Album


class DeezerAlbum(Album):

    @classmethod
    def from_api(cls, data):
        return cls(
            id=int(data['id']),
            title=data['title'],
            artist=data['artist'],
            cover_url=data['cover_xl'],
        )