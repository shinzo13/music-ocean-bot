from app.modules.musicocean.models import Album


class SpotifyAlbum(Album):
    id: str

    @classmethod
    def from_dict(cls, data: dict):
        images = data.get("images") or []
        cover_url = images[0]["url"] if images else None
        return cls(
            id=data["id"],
            title=data["name"],
            artist_name=", ".join(a["name"] for a in data["artists"]),
            cover_url=cover_url,
        )