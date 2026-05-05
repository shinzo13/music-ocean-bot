import re

from bs4 import BeautifulSoup


def _get_track_id(html: str, css_class: str, pattern: str) -> str | None:
    soup = BeautifulSoup(html, "html.parser")

    provider = soup.select_one(css_class)
    if provider:
        match = re.search(pattern, provider["href"])
        if match:
            return match.group(1)
    return None


def get_youtube_id(html: str) -> str | None:
    return _get_track_id(
        html,
        "a.play-this-track-playlink--youtube",
        r"(?:v=|youtu\.be/|embed/)([a-zA-Z0-9_-]{11})"
    )


def get_spotify_id(html: str) -> str | None:
    return _get_track_id(
        html,
        "a.play-this-track-playlink--spotify",
        r"track/([a-zA-Z0-9]+)"
    )
