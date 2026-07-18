from app.modules.musicocean.engines.shared.models import BaseTrackPreview


class SpotifyTrackPreview(BaseTrackPreview):
    id: str
    isrc: str | None = None

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
            preview_url=data.get("preview_url"),
            isrc=(data.get("external_ids") or {}).get("isrc")
        )
