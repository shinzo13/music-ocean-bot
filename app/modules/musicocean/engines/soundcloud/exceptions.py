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