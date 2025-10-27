import json
import re
from typing import Any

from aiohttp import ClientSession

from app.providers.deezer.enums.entity_type import EntityType
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
                raise # TODO separated DeezerAPIException
            return raw_data["data"]

    # kinda similar to _api_request() but it has custom path and certain output type
    # so its better to make another function for that..
    # or maybe i can make base _api_request base func and then _api_method and this one?? TODO
    async def _get_entity_tracks(
        self,
        entity_type: EntityType,
        entity_id: int
    ) -> list[DeezerTrack]:
        async with self.session.get(
            f"{API_URL}/{entity_type}/{entity_id}/tracks"
        ) as resp:
            raw_data = await resp.json()
            if "error" in raw_data:
                raise # TODO separated DeezerAPIException
            return [DeezerTrack.from_api(raw_track) for raw_track in raw_data["data"]]

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

    async def get_album_tracks(self, album_id: int):
        return await self._get_entity_tracks(EntityType.ALBUM, album_id)

    async def get_artist_tracks(self, artist_id: int):
        return await self._get_entity_tracks(EntityType.ARTIST, artist_id)

    async def get_playlist_tracks(self, playlist_id: int):
        return await self._get_entity_tracks(EntityType.PLAYLIST, playlist_id)














