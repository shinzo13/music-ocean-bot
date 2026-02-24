class SpotifyException(Exception):
    pass


class SpotifyDataException(SpotifyException):
    pass


class SpotifyAuthException(SpotifyException):
    pass