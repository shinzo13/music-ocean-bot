from app.modules.musicocean.exceptions import ProviderException, ProviderDataException, ProviderAuthException, \
    ProviderAPIException


class SpotifyException(ProviderException):
    pass

class SpotifyAPIException(ProviderAPIException):
    pass

class SpotifyAuthException(ProviderAuthException):
    pass

class SpotifyDataException(ProviderDataException):
    pass