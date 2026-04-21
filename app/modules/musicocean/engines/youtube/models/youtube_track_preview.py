from typing import Optional

from app.modules.musicocean.engines.shared.models import BaseTrackPreview


class YoutubeTrackPreview(BaseTrackPreview):
    id: str
    title: str
    artist_name: str
    cover_url: Optional[str]