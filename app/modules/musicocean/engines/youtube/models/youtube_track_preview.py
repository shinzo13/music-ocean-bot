from typing import Optional

from app.modules.musicocean.models import TrackPreview


class YoutubeTrackPreview(TrackPreview):
    id: str
    title: str
    artist_name: str
    cover_url: Optional[str]