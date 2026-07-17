from app.modules.musicocean.engines.spotify.models import (
    SpotifyAlbum,
    SpotifyArtist,
    SpotifyPlaylist,
    SpotifyTrackPreview,
)


def test_album_from_dict():
    album = SpotifyAlbum.from_dict({
        "id": "abc",
        "name": "Album Name",
        "artists": [{"name": "A"}, {"name": "B"}],
        "images": [{"url": "https://img/xl"}, {"url": "https://img/s"}],
    })
    assert album.id == "abc"
    assert album.title == "Album Name"
    assert album.artist_name == "A, B"
    assert album.cover_url == "https://img/xl"


def test_artist_from_dict_with_followers():
    artist = SpotifyArtist.from_dict({
        "id": "id1",
        "name": "Artist",
        "images": [{"url": "https://img/p"}],
        "followers": {"total": 1234},
    })
    assert artist.name == "Artist"
    assert artist.photo_url == "https://img/p"
    assert artist.listeners == 1234


def test_playlist_from_dict_track_count():
    pl = SpotifyPlaylist.from_dict({
        "id": "pl1",
        "name": "My Playlist",
        "images": [{"url": "https://img/c"}],
        "tracks": {"total": 50},
    })
    assert pl.title == "My Playlist"
    assert pl.track_count == 50
    assert pl.cover_url == "https://img/c"


def test_playlist_from_dict_defaults_track_count_to_zero():
    pl = SpotifyPlaylist.from_dict({
        "id": "pl1",
        "name": "Empty meta",
        "images": [{"url": "https://img/c"}],
    })
    assert pl.track_count == 0


def test_track_preview_uses_album_cover():
    track = SpotifyTrackPreview.from_dict({
        "id": "t1",
        "name": "Song",
        "artists": [{"name": "X"}],
        "album": {"images": [{"url": "https://img/album"}]},
        "preview_url": "https://p/preview.mp3",
    })
    assert track.title == "Song"
    assert track.artist_name == "X"
    assert track.cover_url == "https://img/album"
    assert track.preview_url == "https://p/preview.mp3"


def test_track_preview_prefers_explicit_cover_url():
    track = SpotifyTrackPreview.from_dict({
        "id": "t1",
        "name": "Song",
        "artists": [{"name": "X"}],
        "cover_url": "https://img/override",
        "album": {"images": [{"url": "https://img/album"}]},
    })
    assert track.cover_url == "https://img/override"


def test_album_without_images_has_no_cover():
    album = SpotifyAlbum.from_dict({
        "id": "abc",
        "name": "No Art",
        "artists": [{"name": "A"}],
        "images": [],
    })
    assert album.cover_url is None


def test_playlist_without_images_has_no_cover():
    pl = SpotifyPlaylist.from_dict({
        "id": "pl1",
        "name": "No Art",
        "images": [],
        "tracks": {"total": 3},
    })
    assert pl.cover_url is None


def test_artist_without_images_has_no_photo():
    artist = SpotifyArtist.from_dict({
        "id": "id1",
        "name": "Artist",
        "images": [],
    })
    assert artist.photo_url is None


def test_track_preview_without_cover_is_none():
    track = SpotifyTrackPreview.from_dict({
        "id": "t1",
        "name": "Song",
        "artists": [{"name": "X"}],
        "album": {"images": []},
    })
    assert track.cover_url is None
    assert track.preview_url is None
