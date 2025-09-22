from app.providers.common.models import Artist


class DeezerArtist(Artist):
    id: int
    name: str
    photo_url: str # not sure
    listeners: int # not sure!!