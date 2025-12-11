import re

from aiohttp import ClientSession

from app.modules.musicocean.engines.soundcloud.constants import API_URL
from app.modules.musicocean.engines.soundcloud.enums.api_method import SoundCloudAPIMethod
from app.modules.musicocean.engines.soundcloud.models import (
    SoundCloudTrackPreview,
    SoundCloudTrack,
    SoundCloudAlbum,
    SoundCloudPlaylist
)
from app.modules.musicocean.engines.soundcloud.models.soundcloud_artist import SoundCloudArtist
from app.modules.musicocean.utils import write_id3


class SoundCloudClient:
    session: ClientSession | None
    client_id: str | None

    def __init__(self):
        self.client_id = None
        self.session = None

    async def _get_client_id(self) -> str:
        async with self.session.get("https://soundcloud.com") as resp:
            text = await resp.text()
            matches = re.findall(
                r"(https://a-v2\.sndcdn\.com/assets/0-[^.]+\.js)",
                text
            )
            if not matches:
                raise
            url = matches[0]
        async with self.session.get(url) as resp:
            text = await resp.text()
            client_id = re.search(
                r"client_id:\"([^\"]+)\"",
                text
            )
            if not client_id:
                raise
        return client_id.group(1)

    async def setup(self):
        self.session = ClientSession(raise_for_status=True)
        self.client_id = await self._get_client_id()

    async def _api_request(
            self,
            method: SoundCloudAPIMethod,
            path: str | None = None,
            **kwargs
    ) -> dict:
        async with self.session.get(
                f"{API_URL}/{method.value}{'/' + path if path else ''}?client_id={self.client_id}",
                params=kwargs,
        ) as resp:
            raw_data = await resp.json()
            if "error" in raw_data:
                raise  # TODO separated exceptions
            return raw_data

    async def search_tracks(self, query: str) -> list[SoundCloudTrackPreview]:
        raw_data = await self._api_request(
            method=SoundCloudAPIMethod.SEARCH_TRACKS,
            q=query
        )
        return [SoundCloudTrackPreview.from_dict(raw_track) for raw_track in raw_data["collection"]]

    async def search_albums(self, query: str) -> list[SoundCloudAlbum]:
        raw_data = await self._api_request(
            method=SoundCloudAPIMethod.SEARCH_ALBUMS,
            q=query
        )
        return [SoundCloudAlbum.from_dict(raw_album) for raw_album in raw_data["collection"]]

    async def search_playlists(self, query: str) -> list[SoundCloudPlaylist]:
        raw_data = await self._api_request(
            method=SoundCloudAPIMethod.SEARCH_PLAYLISTS,
            q=query
        )
        return [SoundCloudPlaylist.from_dict(raw_playlist) for raw_playlist in raw_data["collection"]]

    async def search_artists(self, query: str) -> list[SoundCloudArtist]:
        raw_data = await self._api_request(
            method=SoundCloudAPIMethod.SEARCH_ARTISTS,
            q=query
        )
        return [SoundCloudArtist.from_dict(raw_artist) for raw_artist in raw_data["collection"]]

    async def get_album_tracks(self, album_id: int) -> list[SoundCloudTrackPreview]:
        raw_album = await self._api_request(
            method=SoundCloudAPIMethod.GET_ALBUM,
            path=str(album_id)
        )
        return [SoundCloudTrackPreview.from_dict(raw_track) for raw_track in raw_album["tracks"]]

    async def get_artist_tracks(self, artist_id: int) -> list[SoundCloudTrackPreview]:
        raw_artist = await self._api_request(
            method=SoundCloudAPIMethod.GET_ARTIST,
            path=f"{artist_id}/tracks"
        )
        return [SoundCloudTrackPreview.from_dict(raw_track) for raw_track in raw_artist["collection"]]

    async def get_playlist_tracks(self, playlist_id: int) -> list[SoundCloudTrackPreview]:
        raw_playlist = await self._api_request(
            method=SoundCloudAPIMethod.GET_PLAYLIST,
            path=str(playlist_id)
        )
        return [SoundCloudTrackPreview.from_dict(raw_track) for raw_track in raw_playlist["tracks"]]

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
            raise  # TODO
        async with self.session.get(f"{transcoding['url']}?client_id={self.client_id}") as resp:
            stream_url = (await resp.json())["url"]
        async with self.session.get(stream_url) as resp:
            source = b''
            async for chunk in resp.content.iter_chunked(1024):
                source += chunk

        if track.cover_url:
            async with self.session.get(track.cover_url) as resp:
                cover = await resp.read()
                track.cover = cover

        track.content = write_id3(track, source)

        return track

    async def close(self):
        ...
