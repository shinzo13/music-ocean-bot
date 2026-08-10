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
