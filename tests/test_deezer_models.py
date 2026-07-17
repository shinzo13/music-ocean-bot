from app.modules.musicocean.engines.deezer.models import (
    DeezerAlbum,
    DeezerArtist,
    DeezerPlaylist,
    DeezerTrack,
    DeezerTrackPreview,
)


def test_album_uses_cover_xl_when_present():
    album = DeezerAlbum.from_dict({
        "id": "10",
        "title": "T",
        "artist": {"name": "A"},
        "cover_xl": "https://cdn/xl.jpg",
    })
    assert album.id == 10
    assert album.cover_url == "https://cdn/xl.jpg"


def test_album_falls_back_to_api_cover():
    album = DeezerAlbum.from_dict({
        "id": "10",
        "title": "T",
        "artist": {"name": "A"},
        "cover_xl": None,
    })
    assert album.cover_url == "https://api.deezer.com/album/10/image"


def test_artist_parses_fans_count():
    artist = DeezerArtist.from_dict({
        "id": 7,
        "name": "Artist",
        "picture_xl": "https://cdn/p.jpg",
        "nb_fan": "500",
    })
    assert artist.listeners == 500


def test_artist_without_fans_is_none():
    artist = DeezerArtist.from_dict({
        "id": 7,
        "name": "Artist",
        "picture_xl": "https://cdn/p.jpg",
    })
    assert artist.listeners is None


def test_playlist_track_count_coerced_to_int():
    pl = DeezerPlaylist.from_dict({
        "id": "3",
        "title": "PL",
        "picture_xl": "https://cdn/c.jpg",
        "nb_tracks": "12",
    })
    assert pl.track_count == 12
    assert isinstance(pl.track_count, int)


def test_track_preview_builds_cover_from_album_id():
    prev = DeezerTrackPreview.from_dict({
        "id": "99",
        "title": "Song",
        "artist": {"name": "A"},
        "album": {"id": 555},
        "preview": "https://cdn/preview.mp3",
    })
    assert prev.cover_url == "https://api.deezer.com/album/555/image"
    assert prev.preview_url == "https://cdn/preview.mp3"


def test_track_joins_main_artists():
    track = DeezerTrack.from_dict({
        "SNG_ID": "1",
        "SNG_TITLE": "Song",
        "ALB_ID": "2",
        "TRACK_TOKEN": "tok",
        "SNG_CONTRIBUTORS": {"main_artist": ["A", "B"]},
        "DURATION": "200",
    })
    assert track.artist_name == "A, B"
    assert track.track_token == "tok"
    assert track.cover_url == "https://api.deezer.com/album/2/image"


def test_track_falls_back_to_art_name():
    track = DeezerTrack.from_dict({
        "SNG_ID": "1",
        "SNG_TITLE": "Song",
        "ALB_ID": "2",
        "TRACK_TOKEN": "tok",
        "ART_NAME": "Solo",
        "DURATION": "200",
    })
    assert track.artist_name == "Solo"
