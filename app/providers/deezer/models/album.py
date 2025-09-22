from app.providers.common.models import Album
from app.providers.deezer.models import DeezerArtist


class DeezerAlbum(Album):
    id: int
    title: str
    artist: DeezerArtist
    cover_url: str # not sure