COVER_SIZE = "400x400"

DEFAULT_CODEC = "mp3"
DEFAULT_BITRATE = 320


def build_cover_url(cover_uri: str | None, size: str = COVER_SIZE) -> str | None:
    if not cover_uri:
        return None
    return f"https://{cover_uri.replace('%%', size)}"
