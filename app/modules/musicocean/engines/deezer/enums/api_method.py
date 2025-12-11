from enum import StrEnum


class DeezerAPIMethod(StrEnum):
    SEARCH_TRACKS = 'search/track'
    SEARCH_ALBUMS = 'search/album'
    SEARCH_ARTISTS = 'search/artist'
    SEARCH_PLAYLISTS = 'search/playlist'
