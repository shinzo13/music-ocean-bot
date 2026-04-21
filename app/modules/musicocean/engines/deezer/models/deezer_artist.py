from app.modules.musicocean.engines.shared.models import BaseArtist


class DeezerArtist(BaseArtist):

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            name=data['name'],
            photo_url=data['picture_xl'],
            listeners=int(data['nb_fan']) if 'nb_fan' in data else None,
        )
