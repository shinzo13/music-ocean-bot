import re

from aiohttp import ClientSession

from app.modules.musicocean.engines.soundcloud.constants import API_URL
from app.modules.musicocean.engines.soundcloud.enums.api_method import SoundCloudAPIMethod
from app.modules.musicocean.engines.soundcloud.models import SoundCloudTrackPreview, SoundCloudTrack
from app.modules.musicocean.utils import write_id3

class SoundCloudClient:

    session: ClientSession | None

    def __init__(
        self,
        client_id: str,
    ):
        self.client_id = client_id

        self.session = None

    async def setup(self):
        self.session = ClientSession(raise_for_status=True)

    async def _api_request(
            self,
            method: SoundCloudAPIMethod,
            path: str | None = None,
            **kwargs
    ) -> dict:
        async with self.session.get(
            f"{API_URL}/{method.value}{'/'+path if path else ''}?client_id={self.client_id}",
            params=kwargs,
        ) as resp:
            raw_data = await resp.json()
            if "error" in raw_data:
                raise # TODO separated exceptions
            return raw_data


    async def _get_entity_tracks(self):
        ...
    async def search_tracks(self, query: str) -> list[SoundCloudTrackPreview]:
        raw_data = await self._api_request(
            method=SoundCloudAPIMethod.SEARCH_TRACKS,
            q=query
        )
        return [SoundCloudTrackPreview.from_dict(raw_track) for raw_track in raw_data["collection"]]

    async def search_albums(self, query: str) -> list[...]:
        ...

    async def search_playlists(self, query: str) -> list[...]:
        ...

    async def search_artists(self, query: str) -> list[...]:
        ...

    async def get_album_tracks(self, album_id: int):
        ...

    async def get_artist_tracks(self, artist_id: int):
        ...

    async def get_playlist_tracks(self, playlist_id: int):
        ...

    async def download_track(self, track_id: int) -> SoundCloudTrack:
        raw_data = await self._api_request(
            method=SoundCloudAPIMethod.GET_TRACK,
            path=str(track_id),
        )

        track = SoundCloudTrack.from_dict(raw_data)

        transcoding = next(
            (x for x in raw_data["media"]["transcodings"] if x["format"]["protocol"] == "progressive"),
            None
        )
        if not transcoding:
            raise # TODO
        async with self.session.get(f"{transcoding['url']}?client_id={self.client_id}") as resp:
            stream_url = (await resp.json())["url"]
        async with self.session.get(stream_url) as resp:
            source = b''
            async for chunk in resp.content.iter_chunked(1024):
                source += chunk

        async with self.session.get(track.cover_url) as resp:
            cover = await resp.read()
            track.cover = cover


        track.content = write_id3(track, source)

        return track




    async def close(self):
        ...



