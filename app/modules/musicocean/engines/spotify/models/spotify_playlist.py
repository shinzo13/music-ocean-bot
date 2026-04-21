from app.modules.musicocean.engines.shared.models import BasePlaylist


class SpotifyPlaylist(BasePlaylist):
    id: str

    @classmethod
    def from_dict(cls, data: dict):
        images = data.get("images") or []
        cover_url = images[0]["url"] if images else None
        return cls(
            id=data["id"],
            title=data["name"],
            cover_url=cover_url,
            track_count=data.get("tracks", {}).get("total", 0),
        )