from enum import StrEnum, auto


class LastFMApiMethod(StrEnum):
    GET_USER = "user.getinfo"
    GET_RECENT_TRACKS = "user.getRecentTracks"
    GET_TOP_ARTISTS = "user.getTopArtists"