from app.config.settings import EnginesSettings
from app.modules.musicocean.enums import Engine


def test_nothing_disabled_by_default():
    engines = EnginesSettings()
    assert all(engines.is_enabled(e) for e in Engine)


def test_disabled_engine_is_reported_off():
    engines = EnginesSettings(disabled=["YANDEX"])
    assert not engines.is_enabled(Engine.YANDEX)
    assert engines.is_enabled(Engine.DEEZER)


def test_disabled_names_are_case_insensitive():
    engines = EnginesSettings(disabled=["yandex"])
    assert not engines.is_enabled(Engine.YANDEX)
