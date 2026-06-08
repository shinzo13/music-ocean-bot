from app.modules.musicocean.engines.shared.models import BaseAlbum
from app.modules.musicocean.engines.yandex.constants import build_cover_url


class YandexAlbum(BaseAlbum):

    @classmethod
    def from_obj(cls, album) -> "YandexAlbum":
        return cls(
            id=album.id,
            title=album.title,
            artist_name=", ".join(a.name for a in album.artists) or "Unknown",
            cover_url=build_cover_url(album.cover_uri) or "",
        )
