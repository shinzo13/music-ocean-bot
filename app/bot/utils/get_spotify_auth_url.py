from urllib.parse import urlencode

from app.config import settings

def get_spotify_auth_url(
        user_id: int,
        bot_username: str
) -> str:
    params = {
        "client_id": settings.spotify.client_id.get_secret_value(),
        "response_type": "code",
        "redirect_uri": f"https://t.me/{bot_username}",
        "scope": "user-read-currently-playing user-read-recently-played",
        "state": str(user_id)
    }
    return f"https://accounts.spotify.com/authorize?{urlencode(params)}"