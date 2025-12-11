from app.modules.musicocean.models import Artist


class DeezerArtist(Artist):

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            name=data['name'],
            photo_url=data['picture_xl'],
            listeners=int(data['nb_fan']) if 'nb_fan' in data else None,
        )
