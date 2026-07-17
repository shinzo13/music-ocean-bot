import pytest

from app.bot.constants import (
    DEEZER_EMOJI,
    SOUNDCLOUD_EMOJI,
    SPOTIFY_EMOJI,
    YANDEX_EMOJI,
    YOUTUBE_EMOJI,
)
from app.bot.utils.get_engine_emoji import get_engine_emoji
from app.bot.utils.selected_option import option_selection
from app.modules.musicocean.enums import Engine


@pytest.mark.parametrize(
    "engine, emoji",
    [
        (Engine.DEEZER, DEEZER_EMOJI),
        (Engine.SOUNDCLOUD, SOUNDCLOUD_EMOJI),
        (Engine.YOUTUBE, YOUTUBE_EMOJI),
        (Engine.SPOTIFY, SPOTIFY_EMOJI),
        (Engine.YANDEX, YANDEX_EMOJI),
    ],
)
def test_get_engine_emoji_maps_every_engine(engine, emoji):
    assert get_engine_emoji(engine) == emoji


def test_get_engine_emoji_covers_all_enum_members():
    for engine in Engine:
        assert get_engine_emoji(engine)


def test_get_engine_emoji_rejects_unknown():
    with pytest.raises(ValueError):
        get_engine_emoji("not-an-engine")


def test_option_selection_wraps_when_flagged():
    assert option_selection("Deezer", True) == "[ Deezer ]"


def test_option_selection_plain_when_not_flagged():
    assert option_selection("Deezer", False) == "Deezer"
