from app.modules.musicocean.exceptions import ProviderException, ProviderAuthException, ProviderAPIException, \
    ProviderDataException


class YouTubeException(ProviderException):
    pass

class YouTubeAuthException(ProviderAuthException):
    pass

class YouTubeAPIException(ProviderAPIException):
    pass

class YoutubeDataException(ProviderDataException):
    pass


class YoutubeBlockedException(YoutubeDataException):
    """Youtube refused every client with a bot check. Carries whatever we know
    about the track so it can be looked for elsewhere."""

    def __init__(self, track_id: str, message: str, title: str | None, artist_name: str | None):
        super().__init__(message)
        self.track_id = track_id
        self.title = title
        self.artist_name = artist_name

class YoutubeRefusedException(YoutubeDataException):
    """Youtube refused us for this request — another client or a fresh visitor
    id may still get through."""


class YoutubeUnavailableException(YoutubeDataException):
    """The video itself is gone, private or age-gated: retrying is pointless."""
