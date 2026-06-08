from app.modules.musicocean.exceptions import ProviderException, ProviderDataException, ProviderRestrictionException, \
    ProviderAPIException


class YandexException(ProviderException):
    pass


class YandexAPIException(ProviderAPIException):
    pass


class YandexDataException(ProviderDataException):
    pass


class YandexCountryRestrictionException(ProviderRestrictionException):
    pass
