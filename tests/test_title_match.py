import pytest

from app.modules.musicocean.utils.title_match import (
    artists_match,
    is_usable_artist,
    name_candidates,
    titles_match,
)


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


@pytest.mark.parametrize("left,right", [
    ("Madonna", "Madonna, Lola Leon"),
    ("S3RL", "S3rl"),
    ("Kai Angel", "KAI ANGEL"),
])
def test_matching_artists(left, right):
    assert artists_match(left, right)


def test_different_artists_do_not_match():
    assert not artists_match("Deftones", "Korn")


@pytest.mark.parametrize("artist", ["unknown", "", "Various Artists", None])
def test_useless_artists_are_rejected(artist):
    assert not is_usable_artist(artist)


def test_youtube_title_carries_the_artist():
    # the uploader field says nothing, the title says everything
    assert ("MTC", "S3RL") in name_candidates("MTC - S3RL", "unknown")
    assert ("S3RL", "MTC") in name_candidates("MTC - S3RL", "unknown")


def test_known_artist_is_tried_first():
    assert name_candidates("Sextape", "Deftones")[0] == ("Sextape", "Deftones")


def test_nothing_to_split_and_nobody_to_credit():
    assert name_candidates("credits song", "unknown") == [("credits song", None)]
