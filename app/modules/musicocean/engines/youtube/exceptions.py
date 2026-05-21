from app.modules.musicocean.exceptions import ProviderException, ProviderAuthException, ProviderAPIException


class YouTubeException(ProviderException):
    pass

class YouTubeAuthException(ProviderAuthException):
    pass

class YouTubeAPIException(ProviderAPIException):
    pass