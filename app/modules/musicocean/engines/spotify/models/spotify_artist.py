from app.modules.musicocean.engines.shared.models import BaseArtist


class SpotifyArtist(BaseArtist):
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