import pytest

from app.modules.musicocean.utils.title_match import titles_match


@pytest.mark.parametrize("left,right", [
    ("Агент Паранойи", "Агент Паранойи (prod. by x)"),
    ("губы", "губы [Official Video]"),
    ("The Test", "the test"),
    ("web 2.0", "Web 2.0 (Official Audio)"),
])
def test_matching_titles(left, right):
    assert titles_match(left, right)


@pytest.mark.parametrize("left,right", [
    ("test", "testament"),
    ("Атака", "Атака Титанов"),
    ("The Test", "Test"),
    ("щ", ""),
])
def test_mismatching_titles(left, right):
    assert not titles_match(left, right)
