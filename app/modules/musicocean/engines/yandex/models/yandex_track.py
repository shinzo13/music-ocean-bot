from typing import Optional

from app.modules.musicocean.engines.shared.models import BaseTrack
from app.modules.musicocean.engines.yandex.constants import build_cover_url


class YandexTrack(BaseTrack):
    duration: Optional[int] = None

    @classmethod
    def from_obj(cls, track) -> "YandexTrack":
        return cls(
            id=track.id,
            title=track.title,
            artist_name=", ".join(a.name for a in track.artists) or "Unknown",
            cover_url=build_cover_url(track.cover_uri),
            duration=int(track.duration_ms / 1000) if track.duration_ms else None
        )
