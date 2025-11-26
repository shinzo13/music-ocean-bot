from typing import Union

from app.modules.musicocean.providers import DeezerClient
from app.config.settings import settings
from app.modules.musicocean.enums import Provider
from app.modules.musicocean.providers.deezer.models import (
    DeezerTrackPreview,
    DeezerTrack,
    DeezerAlbum,
    DeezerArtist,
    DeezerPlaylist
)

class MusicOceanClient:
    def __init__(self):

        # TODO as fields
        self.selected_engine = None
        self.ready = False

        self.deezer = None
        self.soundcloud = None
        self.youtube = None
        self.spotify = None

    async def setup_deezer(self, login: str, password: str):
        self.deezer = DeezerClient(
            login=login,
            password=password
        )
        await self.deezer.setup()
        if not self.selected_engine:
            self.selected_engine = self.deezer

    async def setup_all(self):
        if self.deezer:
            await self.deezer.setup()
        # ...
        self.ready = True

    # not sure if async is needed here
    async def set_provider(self, provider: Provider):
        match provider:
            case Provider.DEEZER:
                if not self.deezer:
                    raise "selected provider not specified"
                self.selected_engine = self.deezer
            # ...

    # TODO unions
    async def search_tracks(self, query: str) -> list[DeezerTrackPreview]:
        return await self.selected_engine.search_tracks(query)
    async def search_albums(self, query: str) -> list[DeezerAlbum]:
        return await self.selected_engine.search_albums(query)
    async def search_playlists(self, query: str) -> list[DeezerPlaylist]:
        return await self.selected_engine.search_playlists(query)
    async def search_artists(self, query: str) -> list[DeezerArtist]:
        return await self.selected_engine.search_artists(query)
    async def get_album_tracks(self, album_id: int):
        ...
    async def get_artist_tracks(self, artist_id: int):
        ...
    async def get_playlist_tracks(self, playlist_id: int):
        ...
    async def download_track(self, track_id: int) -> Union[DeezerTrack]:
        return await self.selected_engine.download_track(track_id)
