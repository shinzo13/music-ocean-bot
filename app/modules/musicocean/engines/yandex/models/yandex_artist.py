from app.modules.musicocean.engines.shared.models import BaseArtist
from app.modules.musicocean.engines.yandex.constants import build_cover_url


class YandexArtist(BaseArtist):

    @classmethod
    def from_obj(cls, artist) -> "YandexArtist":
        cover_uri = artist.cover.uri if artist.cover else artist.og_image
        return cls(
            id=artist.id,
            name=artist.name,
            photo_url=build_cover_url(cover_uri) or "",
            listeners=artist.likes_count,
        )
