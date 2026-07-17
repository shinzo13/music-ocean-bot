from app.modules.musicocean.exceptions import (
    MusicOceanException,
    ProviderAPIException,
    ProviderAuthException,
    ProviderDataException,
    ProviderException,
    ProviderRateLimitException,
    ProviderRestrictionException,
)


def test_message_is_stored_and_stringified():
    exc = MusicOceanException("boom")
    assert exc.message == "boom"
    assert str(exc) == "boom"


def test_message_defaults_to_empty():
    assert MusicOceanException().message == ""


def test_provider_exceptions_subclass_hierarchy():
    for cls in (
        ProviderException,
        ProviderAuthException,
        ProviderAPIException,
        ProviderRestrictionException,
        ProviderDataException,
        ProviderRateLimitException,
    ):
        assert issubclass(cls, MusicOceanException)
        assert issubclass(cls, ProviderException) or cls is ProviderException


def test_restriction_is_catchable_as_provider_exception():
    try:
        raise ProviderRestrictionException("region blocked")
    except ProviderException as exc:
        assert exc.message == "region blocked"
