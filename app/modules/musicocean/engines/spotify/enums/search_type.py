from enum import StrEnum


class SpotifySearchType(StrEnum):
    TRACK = "track"
    ALBUM = "album"
    PLAYLIST = "playlist"
    ARTIST = "artist"