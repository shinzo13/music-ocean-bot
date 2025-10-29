from app.musicocean.providers.common.models import Artist


class DeezerArtist(Artist):

    @classmethod
    def from_api(cls, data: dict):
        return cls(
            id=data['id'],
            name=data['name'],
            photo_url=data['picture_xl'],
            listeners=int(data['nb_fan'])
        )