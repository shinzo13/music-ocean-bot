import pytest

from app.bot.callbacks.track_entity_callback import TrackEntity, TrackEntityCallback
from app.bot.keyboards import track_info_keyboard
from app.modules.musicocean.engines.deezer.models import DeezerTrackPreview
from app.modules.musicocean.engines.soundcloud.models import SoundCloudTrackPreview
from app.modules.musicocean.engines.spotify.models import SpotifyTrackPreview
from app.modules.musicocean.enums import Engine

# telegram rejects a whole keyboard whose callback data is over the limit
CALLBACK_LIMIT = 64


def test_callback_round_trip():
    packed = TrackEntityCallback(engine_prefix="dz", entity=TrackEntity.ALBUM, track_id="778484").pack()
    parsed = TrackEntityCallback.unpack(packed)
    assert parsed.engine_prefix == "dz"
    assert parsed.entity is TrackEntity.ALBUM
    assert parsed.track_id == "778484"


@pytest.mark.parametrize("engine,track_id", [
    (Engine.DEEZER, 3054091951),
    (Engine.YOUTUBE, "dE7T2nPP05c"),
    (Engine.SPOTIFY, "1dpHnn6eh4Pz55UproSdJv"),
])
def test_buttons_fit_the_callback_limit(engine, track_id):
    for row in track_info_keyboard(track_id, engine).inline_keyboard:
        assert len(row[0].callback_data.encode()) <= CALLBACK_LIMIT


def test_deezer_track_carries_album_and_artist():
    track = DeezerTrackPreview.from_dict({
        "id": 3054091951,
        "title": "Семейный ужин",
        "artist": {"id": 117231932, "name": "Лев Печеньев"},
        "album": {"id": 659442461},
        "preview": None,
    })
    assert track.album_id == 659442461
    assert track.artist_id == 117231932


def test_soundcloud_track_has_an_artist_but_no_album():
    track = SoundCloudTrackPreview.from_dict({
        "id": 1860887232,
        "title": "Атака",
        "user": {"id": 1410644007, "username": "zavet"},
        "artwork_url": None,
    })
    assert track.artist_id == 1410644007
    # soundcloud has uploaders and playlists, not albums
    assert track.album_id is None


def test_spotify_track_carries_both():
    track = SpotifyTrackPreview.from_dict({
        "id": "1dpHnn6eh4Pz55UproSdJv",
        "name": "так похуй",
        "artists": [{"id": "1Q5COYHgA7ch0y3HqCNgwt", "name": "madk1d"}],
        "album": {"id": "40FhIwRsb0iaAUEinayobc", "images": []},
    })
    assert track.album_id == "40FhIwRsb0iaAUEinayobc"
    assert track.artist_id == "1Q5COYHgA7ch0y3HqCNgwt"


def test_a_track_with_nothing_to_point_at():
    # youtube knows neither, and the handler turns that into an alert rather
    # than a request for album None
    track = SpotifyTrackPreview.from_dict({
        "id": "x",
        "name": "t",
        "artists": [],
        "album": {},
    })
    assert track.album_id is None
    assert track.artist_id is None
