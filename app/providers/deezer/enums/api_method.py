from enum import StrEnum

class DeezerAPIMethod(StrEnum):
    SEARCH_TRACKS = 'search/track'
    SEARCH_ALBUM = 'search/album'
    SEARCH_ARTIST = 'search/artist'
    SEARCH_PLAYLIST = 'search/playlist'