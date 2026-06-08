from app.modules.musicocean.engines.shared.models import BaseTrackPreview
from app.modules.musicocean.engines.yandex.constants import build_cover_url


class YandexTrackPreview(BaseTrackPreview):

    @classmethod
    def from_obj(cls, track) -> "YandexTrackPreview":
        return cls(
            id=track.id,
            title=track.title,
            artist_name=", ".join(a.name for a in track.artists) or "Unknown",
            cover_url=build_cover_url(track.cover_uri),
            preview_url=None
        )
