import re

_NOISE = re.compile(r"\(.*?\)|\[.*?]|\b(official|video|audio|lyrics|prod\.?|feat\.?|ft\.?)\b", re.I)
_NON_WORD = re.compile(r"[^\w\s]", re.U)


def normalize_title(value: str) -> str:
    value = _NOISE.sub(" ", value.lower())
    value = _NON_WORD.sub(" ", value)
    return " ".join(value.split())


def titles_match(left: str, right: str) -> bool:
    a = set(normalize_title(left).split())
    b = set(normalize_title(right).split())
    if not a or not b:
        return False
    return a == b


def artists_match(left: str, right: str) -> bool:
    """Looser than titles: a release credits "Madonna, Lola Leon" where the
    other engine says "Madonna", and both are the same artist. One name being
    contained in the other is enough."""
    a = set(normalize_title(left).split())
    b = set(normalize_title(right).split())
    if not a or not b:
        return False
    return a <= b or b <= a


# youtube hands out an uploader, not an artist: "unknown" and channel names are
# what a track ends up credited to
_NO_ARTIST = {"", "unknown", "various artists", "topic", "auto-generated"}


def is_usable_artist(artist: str | None) -> bool:
    return normalize_title(artist or "") not in _NO_ARTIST


def name_candidates(title: str, artist: str | None) -> list[tuple[str, str | None]]:
    """Ways to read "MTC - S3RL" by "unknown".

    A youtube title routinely carries the artist that its uploader field does
    not, in either order. Both readings are offered, most trustworthy first, so
    the caller can look each one up and keep whichever actually matches.
    """
    out: list[tuple[str, str | None]] = []
    known = is_usable_artist(artist)
    if known:
        out.append((title, artist))

    if " - " in title:
        left, right = (part.strip() for part in title.split(" - ", 1))
        if left and right:
            # "Artist - Title" and "Title - Artist" both happen
            out.append((right, left))
            out.append((left, right))

    if not known:
        out.append((title, None))
    return out
