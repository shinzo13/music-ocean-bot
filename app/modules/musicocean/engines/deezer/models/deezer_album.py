from app.modules.musicocean.models import Album


class DeezerAlbum(Album):

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=int(data['id']),
            title=data['title'],
            artist_name=data['artist']['name'],
            cover_url=data['cover_xl'],
        )
