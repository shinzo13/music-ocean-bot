import pytest

from app.bot.keyboards.download_button import download_keyboard
from app.bot.utils.track_ref import parse_track_ref
from app.database.models.download_context import DownloadContext, DownloadMode, EntityType
from app.modules.musicocean.enums.engine import Engine


def test_search_result_id():
    ref = parse_track_ref("dz_tr_s_778484")
    assert ref.engine is Engine.DEEZER
    assert ref.track_id == 778484
    assert ref.download_context is DownloadContext.SEARCH


def test_entity_context_is_carried():
    ref = parse_track_ref("sp_tr_ea_1dpHnn6eh4Pz55UproSdJv")
    assert ref.engine is Engine.SPOTIFY
    assert ref.track_id == "1dpHnn6eh4Pz55UproSdJv"
    assert ref.entity_type is EntityType.ALBUM
    assert ref.download_mode is DownloadMode.SINGLE


def test_string_ids_stay_strings():
    assert parse_track_ref("yt_tr_s_FJAOc5fFxTU").track_id == "FJAOc5fFxTU"
    assert parse_track_ref("ya_tr_s_123:456").track_id == "123:456"


def test_legacy_id_without_context_code():
    ref = parse_track_ref("dz_tr_778484")
    assert ref.track_id == 778484
    assert ref.download_context is DownloadContext.SEARCH


@pytest.mark.parametrize("ref", [
    "usage_guide",
    "setup_scrobbling",
    "feature_not_available",
    "downloading",
    "dz_tr_s_notanumber",
    "xx_tr_s_1",
    "dz_al_s_1",
])
def test_rejected(ref):
    assert parse_track_ref(ref) is None


def test_button_carries_the_same_ref():
    kb = download_keyboard("dz_tr_s_778484")
    assert kb.inline_keyboard[0][0].callback_data == "dz_tr_s_778484"


def test_button_dropped_when_ref_exceeds_callback_limit():
    assert download_keyboard(f"ya_tr_s_{'x' * 60}") is None
