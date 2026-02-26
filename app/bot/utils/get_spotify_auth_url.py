from urllib.parse import urlencode

from app.config import settings


def get_spotify_auth_url(user_id: int) -> str:
    params = {
        "client_id": settings.spotify.client_id.get_secret_value(),
        "response_type": "code",
        "redirect_uri": f"https://{settings.server.domain}/spotify",
        "scope": "user-read-currently-playing user-read-recently-played",
        "state": str(user_id)
    }
    return f"https://accounts.spotify.com/authorize?{urlencode(params)}"