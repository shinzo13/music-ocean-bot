from app.modules.musicocean.engines.shared.models import BasePlaylist


class DeezerPlaylist(BasePlaylist):

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=int(data["id"]),
            title=data["title"],
            cover_url=data["picture_xl"],
            track_count=int(data["nb_tracks"]),
        )
