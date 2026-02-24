SPOTIFY_API_BASE = "https://api.spotify.com/v1"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_SCROBBLE_URL = (
    "https://accounts.spotify.com/authorize?"
    "client_id={client_id}&"
    "response_type=code&"
    "redirect_uri={redirect_uri}&"
    "scope=user-read-currently-playing%20user-read-recently-played"
)