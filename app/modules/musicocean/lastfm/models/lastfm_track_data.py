from pydantic import BaseModel


class LastFMTrackData(BaseModel):
    title: str
    artist_name: str
    cover_url: str
    lastfm_url: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title=data["name"],
            artist_name=data["artist"]["#text"],
            cover_url=data["image"][2]["#text"],
            lastfm_url=data["url"]
        )
