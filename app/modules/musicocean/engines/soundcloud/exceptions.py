from app.modules.musicocean.exceptions import ProviderException, ProviderAPIException, ProviderDataException, \
    ProviderAuthException


class SoundCloudException(ProviderException):
    pass

class SoundCloudAuthException(ProviderAuthException):
    pass

class SoundCloudAPIException(ProviderAPIException):
    pass

class SoundCloudDataException(ProviderDataException):
    pass


class SoundCloudSnippetException(SoundCloudDataException):
    def __init__(self, title: str, artist_name: str):
        super().__init__(f"soundcloud only serves a 30s snippet of {artist_name} - {title}")
        self.title = title
        self.artist_name = artist_name