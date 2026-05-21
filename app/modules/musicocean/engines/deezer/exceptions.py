from app.modules.musicocean.exceptions import ProviderException, ProviderDataException, ProviderRestrictionException, \
    ProviderAPIException


class DeezerException(ProviderException):
    pass

class DeezerAPIException(ProviderAPIException):
    pass

class DeezerDataException(ProviderDataException):
    pass

class DeezerCountryRestrictionException(ProviderRestrictionException):
    pass