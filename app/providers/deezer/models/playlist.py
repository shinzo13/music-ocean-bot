from app.providers.common.models import Playlist

class DeezerPlaylist(Playlist):
    id: int
    title: str
    cover_url: str
    track_count: int