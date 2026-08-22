"""Every key the code asks for must exist in every locale.

Strings are added by hand to four files, and a key missing from one of them
fails only for the users who happen to have that language — in production,
quietly, long after the change.
"""
import re
from pathlib import Path

import pytest

APP = Path(__file__).resolve().parent.parent / "app"
LOCALES = APP / "locales"

# i18n.get('key'), LazyProxy('key') — the two ways a string is asked for
KEY_CALL = re.compile(r"""(?:i18n\.get|LazyProxy)\(\s*['"]([a-z0-9-]+)['"]""")
# keys built at runtime out of a table are matched by prefix instead
DYNAMIC_PREFIXES = ("feature-",)


def locale_names() -> list[str]:
    return sorted(p.name for p in LOCALES.iterdir() if p.is_dir())


def keys_in(locale: str) -> set[str]:
    text = (LOCALES / locale / "main.ftl").read_text(encoding="utf-8")
    return {
        line.split("=", 1)[0].strip()
        for line in text.splitlines()
        if line and not line.startswith(("#", " ", "\t", ".")) and "=" in line
    }


def keys_used_in_code() -> set[str]:
    used: set[str] = set()
    for path in APP.rglob("*.py"):
        used.update(KEY_CALL.findall(path.read_text(encoding="utf-8")))
    return used


def test_locales_are_present():
    assert set(locale_names()) >= {"en", "ru", "uk", "pl"}


@pytest.mark.parametrize("locale", locale_names())
def test_every_used_key_exists(locale):
    missing = sorted(keys_used_in_code() - keys_in(locale))
    assert not missing, f"{locale} is missing: {missing}"


@pytest.mark.parametrize("locale", locale_names())
def test_locales_agree_with_english(locale):
    # en is the default the middleware falls back to, so it defines the set
    missing = sorted(keys_in("en") - keys_in(locale))
    assert not missing, f"{locale} lacks keys that en has: {missing}"
