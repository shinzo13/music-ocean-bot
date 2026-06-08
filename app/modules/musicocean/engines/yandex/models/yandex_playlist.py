from app.modules.musicocean.engines.shared.models import BasePlaylist
from app.modules.musicocean.engines.yandex.constants import build_cover_url


class YandexPlaylist(BasePlaylist):

    @classmethod
    def from_obj(cls, playlist) -> "YandexPlaylist":
        cover_uri = playlist.cover.uri if playlist.cover else playlist.og_image
        return cls(
            id=f"{playlist.owner.uid}:{playlist.kind}",
            title=playlist.title,
            cover_url=build_cover_url(cover_uri) or "",
            track_count=playlist.track_count or 0,
        )
