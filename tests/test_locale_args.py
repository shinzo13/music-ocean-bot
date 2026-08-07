"""Every i18n call must pass the placeholders its locale strings expect.

A missing one only blows up at runtime, inside the handler, as a
FluentReferenceError — so it is worth catching here instead.
"""
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCALES = ROOT / "app" / "locales"
SOURCES = ROOT / "app"

KEY_LINE = re.compile(r"^([a-zA-Z][\w-]*)\s*=(.*)$")
PLACEHOLDER = re.compile(r"\{\s*\$(\w+)")
CALL = re.compile(
    r"(?:i18n\.get|LazyProxy)\(\s*['\"]([\w-]+)['\"]\s*(,[^()]*(?:\([^()]*\)[^()]*)*)?\)",
    re.S,
)
KWARG = re.compile(r"(\w+)\s*=")


def locale_placeholders() -> dict[str, dict[str, set[str]]]:
    """key -> locale -> placeholders used by that translation."""
    keys: dict[str, dict[str, set[str]]] = defaultdict(dict)
    for path in LOCALES.glob("*/main.ftl"):
        bodies: dict[str, str] = defaultdict(str)
        current = None
        for line in path.read_text(encoding="utf-8").splitlines():
            match = KEY_LINE.match(line)
            if match:
                current = match.group(1)
                bodies[current] += match.group(2)
            elif current and line.startswith((" ", "\t")):
                bodies[current] += "\n" + line
            elif line.strip():
                current = None
        for key, text in bodies.items():
            keys[key][path.parent.name] = set(PLACEHOLDER.findall(text))
    return keys


def test_every_i18n_call_passes_the_placeholders_its_locales_need():
    keys = locale_placeholders()
    assert keys, "no locale keys parsed — check the locales path"

    problems = []
    for path in SOURCES.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        for match in CALL.finditer(source):
            key, args = match.group(1), match.group(2) or ""
            if key not in keys:
                problems.append(f"{path.relative_to(ROOT)}: unknown key '{key}'")
                continue
            passed = set(KWARG.findall(args))
            for locale, needed in keys[key].items():
                missing = needed - passed
                if missing:
                    line = source[: match.start()].count("\n") + 1
                    problems.append(
                        f"{path.relative_to(ROOT)}:{line}: '{key}' [{locale}] "
                        f"misses {sorted(missing)}"
                    )

    assert not problems, "i18n placeholders not passed:\n" + "\n".join(sorted(set(problems)))
