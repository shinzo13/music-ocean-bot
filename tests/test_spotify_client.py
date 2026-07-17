import time

import pytest

from app.modules.musicocean.engines.spotify.client import SpotifyClient
from app.modules.musicocean.engines.spotify.exceptions import (
    SpotifyAPIException,
    SpotifyAuthException,
    SpotifyDataException,
)


class FakeResp:
    def __init__(self, payload):
        self._payload = payload

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    async def json(self):
        return self._payload


class FakeSession:
    def __init__(self, get_responses=None, post_responses=None):
        self.get_responses = list(get_responses or [])
        self.post_responses = list(post_responses or [])
        self.get_calls = []
        self.post_calls = []

    def get(self, url, headers=None, params=None):
        self.get_calls.append({"url": url, "headers": headers, "params": params})
        return FakeResp(self.get_responses.pop(0))

    def post(self, url, headers=None, data=None):
        self.post_calls.append({"url": url, "headers": headers, "data": data})
        return FakeResp(self.post_responses.pop(0))


def make_client(get_responses=None, post_responses=None, token="tok",
                valid=True):
    client = SpotifyClient(client_id="id", client_secret="secret", yt=None)
    client.session = FakeSession(get_responses, post_responses)
    client._access_token = token
    client._token_expires_at = time.monotonic() + (1000 if valid else -1)
    return client


async def test_get_returns_payload_and_sends_bearer_token():
    client = make_client(get_responses=[{"tracks": {"items": []}}])
    data = await client._get("search", q="x", type="track")
    assert data == {"tracks": {"items": []}}
    call = client.session.get_calls[0]
    assert call["headers"]["Authorization"] == "Bearer tok"


async def test_get_drops_none_params():
    client = make_client(get_responses=[{"ok": True}])
    await client._get("tracks/1", market="US", extra=None)
    assert client.session.get_calls[0]["params"] == {"market": "US"}


async def test_get_404_raises_data_exception():
    client = make_client(
        get_responses=[{"error": {"status": 404, "message": "not here"}}]
    )
    with pytest.raises(SpotifyDataException):
        await client._get("tracks/missing")


async def test_get_403_raises_api_exception():
    # the playlist-tracks / artist-top-tracks case
    client = make_client(
        get_responses=[{"error": {"status": 403, "message": "Forbidden"}}]
    )
    with pytest.raises(SpotifyAPIException):
        await client._get("playlists/x/tracks")


async def test_get_401_refreshes_token_and_retries():
    client = make_client(
        get_responses=[
            {"error": {"status": 401, "message": "expired"}},
            {"ok": True},
        ],
        post_responses=[{"access_token": "fresh", "expires_in": 3600}],
    )
    data = await client._get("tracks/1")
    assert data == {"ok": True}
    assert client._access_token == "fresh"
    assert len(client.session.post_calls) == 1
    assert len(client.session.get_calls) == 2


async def test_refresh_token_updates_token_and_expiry():
    client = make_client(
        post_responses=[{"access_token": "abc", "expires_in": 3600}],
        valid=False,
    )
    before = time.monotonic()
    await client._refresh_token()
    assert client._access_token == "abc"
    assert client._token_expires_at > before


async def test_refresh_token_without_access_token_raises():
    client = make_client(
        post_responses=[{"error": "invalid_client",
                         "error_description": "bad creds"}],
        valid=False,
    )
    with pytest.raises(SpotifyAuthException):
        await client._refresh_token()


async def test_ensure_token_refreshes_only_when_expired():
    valid = make_client(post_responses=[], valid=True)
    await valid._ensure_token()  # must not touch session.post (empty queue)
    assert valid.session.post_calls == []

    expired = make_client(
        post_responses=[{"access_token": "new", "expires_in": 3600}],
        valid=False,
    )
    await expired._ensure_token()
    assert expired._access_token == "new"
