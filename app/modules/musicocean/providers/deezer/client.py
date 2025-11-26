import json
import re

from aiohttp import ClientSession

from app.modules.musicocean.providers.deezer.enums.entity_type import EntityType
from app.modules.musicocean.providers.deezer.models import DeezerTrack, DeezerTrackPreview, DeezerAlbum, DeezerPlaylist, DeezerArtist
from app.modules.musicocean.providers.deezer.utils import decrypt_track, get_arl
from app.modules.musicocean.providers.deezer.enums import DeezerAPIMethod
from app.modules.musicocean.providers.deezer.constants import *
from app.modules.musicocean.providers.deezer.utils import write_id3


class DeezerClient:
    def __init__(
            self,
            login: str,
            password: str,
            proxies: dict[str, str] = None # TODO
    ):
        self.login = login
        self.password = password

        self.session = None
        self.arl = None
        self.license_token = None
    async def setup(self):
        self.arl = await get_arl(
            self.login,
            self.password,
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

    async def search_tracks(self, query: str) -> list[DeezerTrackPreview]:
        raw_data = await self._api_request(
            method=DeezerAPIMethod.SEARCH_TRACKS,
            q=query
        )
        return [DeezerTrackPreview.from_dict(raw_track) for raw_track in raw_data]

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

    async def _get_client_track(self, track_id: int):
        async with self.session.get(
            ITEM_URL.format(
                type="track",
                id=track_id
            )
        ) as resp:
            match = re.search(DATA_PATTERN, await resp.text(), re.DOTALL).group(1)
        return DeezerTrack.from_dict(json.loads(match)["DATA"])

    async def _get_track_url(self, track_token: str) -> str:
        async with self.session.post(
            MEDIA_URL,
            json={
                'license_token': self.license_token,
                'media': [{'type': "FULL", "formats": [{
                    "cipher": "BF_CBC_STRIPE",
                    "format": "MP3_128"  # TODO
                }]}],
                'track_tokens': [track_token]
            }
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()
        url = data['data'][0]['media'][0]['sources'][0]['url']
        return url

    async def download_track(self, track_id: int) -> DeezerTrack:
        track = await self._get_client_track(track_id)

        # TODO: country restriction handling

        track_url = await self._get_track_url(track.track_token)
        async with self.session.get(track_url) as resp:
            track_bytes = await decrypt_track(resp, track.id)

        async with self.session.get(track.cover_url) as resp:
            resp.raise_for_status()
            cover = await resp.read()

        track.cover = cover
        track.content = write_id3(
            track=track,
            source=track_bytes
        )

        return track

    async def close(self):
        await self.session.close()



