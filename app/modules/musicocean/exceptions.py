class MusicOceanException(Exception):
    def __init__(self, message: str = "", *args):
        self.message = message
        super().__init__(message, *args)

class ProviderException(MusicOceanException):
    pass

class ProviderAuthException(ProviderException):
    pass

class ProviderAPIException(ProviderException):
    pass

class ProviderRestrictionException(ProviderException):
    pass

class ProviderDataException(ProviderException):
    pass

class ProviderRateLimitException(ProviderException):
    pass