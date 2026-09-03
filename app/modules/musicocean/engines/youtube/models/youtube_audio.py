from pydantic import BaseModel


class YoutubeAudio(BaseModel):
    """What the downloader knows about a video after pulling its audio."""

    title: str
    artist_name: str
    duration: int
    thumbnail_url: str
