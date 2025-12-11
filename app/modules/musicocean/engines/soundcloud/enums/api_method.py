from enum import Enum

class SoundCloudAPIMethod(Enum):
    SEARCH_TRACKS = 'search/tracks'
    SEARCH_ALBUMS = 'search/albums'
    SEARCH_ARTISTS = 'search/users'
    SEARCH_PLAYLISTS = 'search/playlists_without_albums'

    GET_TRACK = 'tracks'
    GET_ALBUM = 'playlists'
    GET_PLAYLIST = 'playlists'
    GET_ARTIST = 'users'