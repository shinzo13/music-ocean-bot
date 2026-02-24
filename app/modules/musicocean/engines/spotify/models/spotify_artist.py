from app.modules.musicocean.models import Artist


class SpotifyArtist(Artist):
    id: str

    @classmethod
    def from_dict(cls, data: dict):
        images = data.get("images") or []
        photo_url = images[0]["url"] if images else None
        return cls(
            id=data["id"],
            name=data["name"],
            photo_url=photo_url,
            listeners=data.get("followers", {}).get("total"),
        )