from app.modules.musicocean.enums import Engine, EntityType


def test_engine_is_str_enum():
    assert Engine.DEEZER == "DEEZER"
    assert Engine("SPOTIFY") is Engine.SPOTIFY


def test_engine_members():
    assert {e.value for e in Engine} == {
        "DEEZER",
        "SOUNDCLOUD",
        "YOUTUBE",
        "SPOTIFY",
        "YANDEX",
    }


def test_entity_type_values():
    assert EntityType.ALBUM == "album"
    assert {e.value for e in EntityType} == {"album", "artist", "playlist"}
