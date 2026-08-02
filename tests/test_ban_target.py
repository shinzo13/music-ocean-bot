import pytest

from app.bot.handlers.admin_panel.ban_user import parse_target, user_label
from app.database.models import User
from app.database.models.user import UserSettings


@pytest.mark.parametrize("text, expected", [
    ("123456", ("id", "123456")),
    ("  123456  ", ("id", "123456")),
    ("-100500", ("id", "-100500")),
    ("@vasya", ("username", "vasya")),
    (" @vasya ", ("username", "vasya")),
    ("vasya", ("username", "vasya")),
    ("@user123", ("username", "user123")),
    ("", ("username", "")),
])
def test_parse_target(text, expected):
    assert parse_target(text) == expected


def _user(**kwargs) -> User:
    defaults = dict(
        user_id=1, first_name=None, last_name=None, username=None,
        settings=UserSettings()
    )
    return User(**{**defaults, **kwargs})


def test_user_label_prefers_username():
    assert user_label(_user(username="vasya", first_name="Vasya")) == "@vasya"


def test_user_label_falls_back_to_name_then_id():
    assert user_label(_user(first_name="Vasya", last_name="Pupkin")) == "Vasya Pupkin"
    assert user_label(_user(user_id=42)) == "42"
