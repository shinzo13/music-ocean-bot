import pytest

from app.bot.handlers.inline_search.link_search import (
    DEEZER_REGEX,
    SPOTIFY_REGEX,
    YANDEX_ALBUM_REGEX,
    YANDEX_ARTIST_REGEX,
    YANDEX_PLAYLIST_REGEX,
    YANDEX_REGEX,
    YANDEX_TRACK_REGEX,
    YOUTUBE_REGEX,
)


@pytest.mark.parametrize(
    "url, entity_type, entity_id",
    [
        ("https://deezer.com/track/123", "track", "123"),
        ("https://www.deezer.com/album/456", "album", "456"),
        ("https://deezer.com/en/playlist/789", "playlist", "789"),
        ("https://deezer.com/fr/artist/42", "artist", "42"),
    ],
)
def test_deezer_regex_extracts_type_and_id(url, entity_type, entity_id):
    m = DEEZER_REGEX.search(url)
    assert m is not None
    assert m.groups() == (entity_type, entity_id)


@pytest.mark.parametrize(
    "url, entity_type, entity_id",
    [
        ("https://open.spotify.com/track/6rqhFgbbKwnb9MLmUQDhG6", "track",
         "6rqhFgbbKwnb9MLmUQDhG6"),
        ("https://open.spotify.com/album/1DFixLWuPkv3KT3TnV35m3", "album",
         "1DFixLWuPkv3KT3TnV35m3"),
        ("https://open.spotify.com/playlist/1jJFMBm7TFbJ5GCw1a7cnf", "playlist",
         "1jJFMBm7TFbJ5GCw1a7cnf"),
        ("https://open.spotify.com/artist/0TnOYISbd1XYRBk9myaseg", "artist",
         "0TnOYISbd1XYRBk9myaseg"),
    ],
)
def test_spotify_regex_extracts_type_and_id(url, entity_type, entity_id):
    m = SPOTIFY_REGEX.search(url)
    assert m is not None
    assert m.groups() == (entity_type, entity_id)


def test_spotify_regex_ignores_query_suffix():
    m = SPOTIFY_REGEX.search(
        "https://open.spotify.com/playlist/1jJFMBm7TFbJ5GCw1a7cnf?si=abc123"
    )
    assert m.group(2) == "1jJFMBm7TFbJ5GCw1a7cnf"


@pytest.mark.parametrize(
    "url",
    [
        "https://spotify.com/track/123",  # missing open. subdomain
        "not a link at all",
        "https://open.spotify.com/episode/123",  # unsupported entity
    ],
)
def test_spotify_regex_rejects_bad_links(url):
    assert SPOTIFY_REGEX.search(url) is None


@pytest.mark.parametrize(
    "url, video_id",
    [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
    ],
)
def test_youtube_regex(url, video_id):
    m = YOUTUBE_REGEX.search(url)
    assert m is not None
    assert m.group(1) == video_id


def test_yandex_domain_matches_regional_tlds():
    for tld in ("ru", "com", "by", "kz", "uz"):
        assert YANDEX_REGEX.search(f"https://music.yandex.{tld}/album/1")


def test_yandex_track_regex():
    m = YANDEX_TRACK_REGEX.search(
        "https://music.yandex.ru/album/123/track/456"
    )
    assert m.group(1) == "456"


def test_yandex_album_regex():
    m = YANDEX_ALBUM_REGEX.search("https://music.yandex.ru/album/123")
    assert m.group(1) == "123"


def test_yandex_artist_regex():
    m = YANDEX_ARTIST_REGEX.search("https://music.yandex.ru/artist/99")
    assert m.group(1) == "99"


def test_yandex_playlist_regex_extracts_owner_and_id():
    m = YANDEX_PLAYLIST_REGEX.search(
        "https://music.yandex.ru/users/some.user/playlists/1000"
    )
    assert m.groups() == ("some.user", "1000")
