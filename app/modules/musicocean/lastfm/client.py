from typing import Optional

from aiohttp import ClientSession, ClientResponseError

from app.modules.musicocean.enums import Engine
from app.modules.musicocean.lastfm.constants import BASE_URL, HEADERS, GET_TRACK_RETRY_COUNT
from app.modules.musicocean.lastfm.enums.lastfm_api_method import LastFMApiMethod
from app.modules.musicocean.lastfm.exceptions import LastFMNoDataException, LastFMNoProvidersException, \
    LastFMServerException
from app.modules.musicocean.lastfm.models.lastfm_track_data import LastFMTrackData
from app.modules.musicocean.lastfm.models.lastfm_track_preview import LastFMTrackPreview
from app.modules.musicocean.lastfm.utils.get_track_id import get_youtube_id, get_spotify_id


class LastFMClient:

    def __init__(self, api_key: str):
        self.session: Optional[ClientSession] = None
        self.api_key = api_key

    async def setup(self):
        self.session = ClientSession(
            headers=HEADERS,
            raise_for_status=False
        )

    async def _api_request(
            self,
            method: LastFMApiMethod,
            **kwargs
    ) -> dict:
        async with self.session.get(
                url=BASE_URL,
                params=kwargs | {
                    "method": method,
                    "api_key": self.api_key,
                    "format": "json"
                }
        ) as resp:
            return await resp.json()

    async def check_user(self, username: str) -> bool:
        data = await self._api_request(
            method=LastFMApiMethod.GET_USER,
            user=username
        )
        return bool(data)

    async def get_recent_track_data(
            self,
            username: str
    ) -> LastFMTrackData:
        data = await self._api_request(
            method=LastFMApiMethod.GET_RECENT_TRACKS,
            user=username,
            limit=1
        )
        recent = (data or {}).get("recenttracks", {}).get("track")
        if not recent:
            raise LastFMNoDataException()
        track = recent[0] if isinstance(recent, list) else recent
        return LastFMTrackData.from_dict(track)

    async def get_provider_track(
            self,
            track_data: LastFMTrackData
    ) -> tuple[Engine, LastFMTrackPreview]:
        html = None
        # lastfm kinda likes to answer with 502 gateway for no reason
        for _ in range(GET_TRACK_RETRY_COUNT):
            try:
                async with self.session.get(track_data.lastfm_url) as resp:
                    html = await resp.text()
            except ClientResponseError:
                continue
        if not html:
            raise LastFMServerException()

        yt_track_id = get_youtube_id(html)
        if yt_track_id is not None:
            return Engine.YOUTUBE, LastFMTrackPreview.from_track_data(yt_track_id, track_data)

        sp_track_id = get_spotify_id(html)
        if sp_track_id is not None:
            return Engine.SPOTIFY, LastFMTrackPreview.from_track_data(sp_track_id, track_data)

        raise LastFMNoProvidersException()

    async def get_top_artists(self, username: str):
        data = await self._api_request(
            method=LastFMApiMethod.GET_TOP_ARTISTS,
            period="overall",
            user=username,
        )
        artists = {
            artist["name"]: int(artist["playcount"])
            for artist in data["topartists"]["artist"]
        }

        ...
