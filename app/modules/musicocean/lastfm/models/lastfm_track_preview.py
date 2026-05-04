from app.modules.musicocean.engines.shared.models import BaseTrack, BaseTrackPreview
from app.modules.musicocean.lastfm.models.lastfm_track_data import LastFMTrackData


# эта хуйня будеи мимикрировать под ютуб/спотифай треки..
class LastFMTrackPreview(BaseTrackPreview):
    id: str
    title: str
    artist_name: str
    cover_url: str

    @classmethod
    def from_track_data(cls, track_id: str, data: LastFMTrackData):
        return cls(
            id=track_id,
            title=data.title,
            artist_name=data.artist_name,
            cover_url=data.cover_url
        )
