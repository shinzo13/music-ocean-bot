import pytest

from app.modules.musicocean.engines.youtube.exceptions import (
    YoutubeDataException,
    YoutubeRefusedException,
    YoutubeUnavailableException,
)
from app.modules.musicocean.engines.youtube.player import InnertubePlayer, PlayerInfo


def player_payload(formats=None, status="OK", reason=None):
    return {
        "playabilityStatus": {"status": status, **({"reason": reason} if reason else {})},
        "streamingData": {"adaptiveFormats": formats if formats is not None else [
            {"itag": 139, "mimeType": 'audio/mp4; codecs="mp4a.40.5"', "bitrate": 50000,
             "url": "https://stream/139", "contentLength": "1000"},
            {"itag": 140, "mimeType": 'audio/mp4; codecs="mp4a.40.2"', "bitrate": 130000,
             "url": "https://stream/140", "contentLength": "2000"},
            {"itag": 251, "mimeType": 'audio/webm; codecs="opus"', "bitrate": 150000,
             "url": "https://stream/251", "contentLength": "2100"},
        ]},
        "videoDetails": {
            "title": "Creep",
            "author": "Radiohead - Topic",
            "lengthSeconds": "239",
            "thumbnail": {"thumbnails": [
                {"url": "https://img/small"}, {"url": "https://img/large"}]},
        },
    }


CLIENT = {"name": "TEST", "id": 1, "ua": "test-agent",
          "context": {"clientName": "TEST", "clientVersion": "1.0"}}


class FakeResp:
    def __init__(self, status=200, payload=None, body=b""):
        self.status = status
        self._payload = payload
        self._body = body

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    async def json(self):
        return self._payload

    async def read(self):
        return self._body


class FakeSession:
    """Serves the ranges of one blob, and records what was asked for."""

    def __init__(self, blob=b"", status=200):
        self.blob = blob
        self.status = status
        self.range_calls = []

    def get(self, url, headers=None, timeout=None):
        start, end = url.split("&range=")[1].split("-")
        start, end = int(start), int(end)
        self.range_calls.append((start, end, (headers or {}).get("User-Agent")))
        return FakeResp(status=self.status, body=self.blob[start:end + 1])


def make_player(session=None):
    async def visitor(force=False):
        return "visitor-id"

    return InnertubePlayer(session or FakeSession(), visitor)


def test_parse_picks_the_highest_bitrate_mp4_and_cleans_the_author():
    info = InnertubePlayer._parse("vid", player_payload(), CLIENT)
    assert (info.itag, info.audio_size) == (140, 2000)
    assert info.author == "Radiohead"
    assert info.title == "Creep"
    assert info.duration == 239
    # the largest thumbnail is the last one youtube lists
    assert info.thumbnail_url == "https://img/large"
    assert info.user_agent == "test-agent"


def test_parse_ignores_formats_without_a_plain_url():
    payload = player_payload(formats=[
        {"itag": 140, "mimeType": "audio/mp4", "bitrate": 130000,
         "signatureCipher": "s=...", "contentLength": "2000"},
    ])
    with pytest.raises(YoutubeRefusedException):
        InnertubePlayer._parse("vid", payload, CLIENT)


def test_parse_treats_a_bot_check_as_refusal_worth_retrying():
    payload = player_payload(status="LOGIN_REQUIRED",
                             reason="Sign in to confirm you're not a bot")
    with pytest.raises(YoutubeRefusedException):
        InnertubePlayer._parse("vid", payload, CLIENT)


def test_parse_treats_an_age_gate_as_unavailable():
    payload = player_payload(status="LOGIN_REQUIRED",
                             reason="Sign in to confirm your age")
    with pytest.raises(YoutubeUnavailableException):
        InnertubePlayer._parse("vid", payload, CLIENT)


def test_parse_treats_a_removed_video_as_unavailable():
    payload = player_payload(status="UNPLAYABLE", reason="This video is not available")
    with pytest.raises(YoutubeUnavailableException):
        InnertubePlayer._parse("vid", payload, CLIENT)


def test_parse_rejects_an_answer_without_a_title():
    payload = player_payload()
    payload["videoDetails"]["title"] = ""
    with pytest.raises(YoutubeDataException):
        InnertubePlayer._parse("vid", payload, CLIENT)


def info_for(size, url="https://stream/140"):
    return PlayerInfo(id="vid", title="t", author="a", duration=1,
                      thumbnail_url="", itag=140, audio_url=url,
                      audio_size=size, user_agent="test-agent")


async def test_download_reassembles_ranges_in_order():
    blob = bytes(range(256)) * 20_000  # a few chunks worth
    session = FakeSession(blob)
    player = make_player(session)

    raw = await player.download(info_for(len(blob)))

    assert raw == blob
    # every byte asked for exactly once, and the requests keep the client's agent
    assert sum(end - start + 1 for start, end, _ in session.range_calls) == len(blob)
    assert {ua for _, _, ua in session.range_calls} == {"test-agent"}


async def test_download_retries_a_chunk_that_was_refused_once():
    blob = b"x" * 4096

    class FlakySession(FakeSession):
        def get(self, url, headers=None, timeout=None):
            self.range_calls.append(url)
            if len(self.range_calls) == 1:
                return FakeResp(status=403)
            start, end = url.split("&range=")[1].split("-")
            return FakeResp(body=self.blob[int(start):int(end) + 1])

    session = FlakySession(blob)
    raw = await make_player(session).download(info_for(len(blob)))

    assert raw == blob
    assert len(session.range_calls) == 2


async def test_download_rejects_a_truncated_transfer():
    session = FakeSession(b"only-this")
    player = make_player(session)

    with pytest.raises(YoutubeRefusedException):
        await player.download(info_for(9_000_000))


async def test_download_refuses_when_the_stream_answers_with_an_error():
    session = FakeSession(b"x" * 100, status=403)
    player = make_player(session)

    with pytest.raises(YoutubeRefusedException):
        await player.download(info_for(100))


async def test_info_retries_the_next_client_and_refreshes_the_visitor_id():
    calls = []
    forced = []

    async def visitor(force=False):
        forced.append(force)
        return "fresh" if force else "stale"

    player = InnertubePlayer(FakeSession(), visitor)

    async def fake_player(video_id, client, visitor_id):
        calls.append((client["name"], visitor_id))
        if len(calls) < 3:
            return player_payload(status="LOGIN_REQUIRED",
                                  reason="Sign in to confirm you're not a bot")
        return player_payload()

    player._player = fake_player
    info = await player.info("vid")

    assert info.itag == 140
    # both clients tried on the stale id, then the retry pass got a fresh one
    assert [c[1] for c in calls] == ["stale", "stale", "fresh"]
    assert forced == [False, True]


async def test_info_gives_up_immediately_on_an_unavailable_video():
    calls = []

    async def visitor(force=False):
        return "visitor-id"

    player = InnertubePlayer(FakeSession(), visitor)

    async def fake_player(video_id, client, visitor_id):
        calls.append(client["name"])
        return player_payload(status="UNPLAYABLE", reason="This video is not available")

    player._player = fake_player

    with pytest.raises(YoutubeUnavailableException):
        await player.info("vid")
    assert len(calls) == 1
