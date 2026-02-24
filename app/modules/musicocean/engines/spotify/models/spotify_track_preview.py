from app.modules.musicocean.models import TrackPreview


class SpotifyTrackPreview(TrackPreview):
    id: str

    @classmethod
    def from_dict(cls, data: dict):
        if data.get("cover_url"):
            cover_url = data["cover_url"]
        else:
            images = data.get("album", {}).get("images") or []
            cover_url = images[0]["url"] if images else None
        return cls(
            id=data["id"],
            title=data["name"],
            artist_name=", ".join(a["name"] for a in data["artists"]),
            cover_url=cover_url,
            preview_url=data.get("preview_url")
        )