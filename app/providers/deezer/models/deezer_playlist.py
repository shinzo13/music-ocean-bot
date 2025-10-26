from app.providers.common.models import Playlist

class DeezerPlaylist(Playlist):

    @classmethod
    def from_api(cls, data: dict):
        return cls(
            id=int(data["id"]),
            title=data["title"],
            cover_url=data["picture_xl"],
            track_count=int(data["nb_tracks"]),
        )