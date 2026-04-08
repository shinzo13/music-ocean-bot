from urllib.parse import urlencode

from app.config import settings


def get_lastfm_auth_url(user_id: int) -> str:
    params = {
        "api_key": settings.lastfm.api_key,
        "cb": f"https://{settings.server.domain}/spotify/{user_id}",
    }
    return f"http://www.last.fm/api/auth/?{urlencode(params)}"