import json
import re
from typing import Any

from aiohttp import ClientSession

from app.providers.deezer.models import DeezerTrack, DeezerAlbum, DeezerPlaylist, DeezerArtist
from app.providers.deezer.utils import get_arl
from app.providers.deezer.enums import DeezerAPIMethod
from app.providers.deezer.constants import *

class DeezerClient:
    def __init__(
            self,
            login: str,
            passwd: str,
            proxies: dict[str, str] = None # TODO
    ):
        self.login = login
        self.passwd = passwd

        self.session = None
        self.arl = None
        self.license_token = None
    async def setup(self):
        self.arl = await get_arl(
            self.login,
            self.passwd,
        )
        self.session = ClientSession(
            cookies={
                'arl': self.arl,
                'comeback': '1'
            },
            headers=HEADERS,
            raise_for_status=True
        )

        options = (await (await self.session.get(
            USERDATA_URL
        )).json())['results']['USER']['OPTIONS']
        self.license_token = options['license_token']

    async def _api_request(
        self,
        method: DeezerAPIMethod,
        **kwargs
    ) -> dict:
        async with self.session.get(
            f"{API_URL}/{method}",
            params=kwargs
        ) as resp:
            raw_data = await resp.json()
            if "error" in raw_data:
                raise # TODO separeted DeezerAPIException
            return raw_data # TODO data processing

    async def _get_client_track(self, track_id: int):
        async with self.session.get(
            ITEM_URL.format(
                type="track",
                id=track_id
            )
        ) as resp:
            match = re.search(DATA_PATTERN, await resp.text(), re.DOTALL).group(1)
        return DeezerTrack.from_client(json.loads(match))

    async def search_tracks(self, query: str) -> list[DeezerTrack]:
        raw_data = await self._api_request(
            method=DeezerAPIMethod.SEARCH_TRACKS,
            q=query
        )
        return [DeezerTrack.from_api(raw_track) for raw_track in raw_data]

    async def search_albums(self, query: str) -> list[DeezerAlbum]:
        raw_data = await self._api_request(
            method=DeezerAPIMethod.SEARCH_ALBUMS,
            q=query
        )
        return [DeezerAlbum.from_api(raw_album) for raw_album in raw_data]

    async def search_playlists(self, query: str) -> list[DeezerPlaylist]:
        raw_data = await self._api_request(
            method=DeezerAPIMethod.SEARCH_PLAYLISTS,
            q=query
        )
        return [DeezerPlaylist.from_api(raw_playlist) for raw_playlist in raw_data]

    async def search_artists(self, query: str) -> list[DeezerArtist]:
        raw_data = await self._api_request(
            method=DeezerAPIMethod.SEARCH_ARTISTS,
            q=query
        )
        return [DeezerArtist.from_api(raw_artist) for raw_artist in raw_data]

















