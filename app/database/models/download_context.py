from enum import Enum


class DownloadContext(str, Enum):
    SEARCH = "SEARCH"
    LINK = "LINK"
    LASTFM = "LASTFM"
    ENTITY = "ENTITY"


class EntityType(str, Enum):
    ALBUM = "ALBUM"
    PLAYLIST = "PLAYLIST"
    ARTIST = "ARTIST"


class DownloadMode(str, Enum):
    SINGLE = "SINGLE"
    MULTI = "MULTI"
