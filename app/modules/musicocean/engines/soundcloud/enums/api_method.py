from enum import Enum

class SoundCloudAPIMethod(Enum):
    SEARCH_TRACKS = 'search/tracks'
    SEARCH_ALBUMS = '...'
    SEARCH_ARTISTS = '...'
    SEARCH_PLAYLISTS = '...'

    GET_TRACK = 'tracks'