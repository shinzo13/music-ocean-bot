from enum import Enum


class Engine(str, Enum):
    DEEZER = "DEEZER"
    SOUNDCLOUD = "SOUNDCLOUD"
    YOUTUBE = "YOUTUBE"
    SPOTIFY = "SPOTIFY"
