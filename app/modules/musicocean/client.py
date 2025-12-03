from typing import Union

from app.modules.musicocean.providers import DeezerClient
from app.modules.musicocean.enums.engine import Engine
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


    def _get_engine(self, engine: Engine):
        match engine:
            case Engine.DEEZER:
                return self.deezer
            case Engine.SOUNDCLOUD:
                return self.soundcloud
            case Engine.YOUTUBE:
                return self.youtube
            case Engine.SPOTIFY:
                return self.spotify
        return None


    async def search_tracks(self, engine: Engine, query: str) -> Union[list[DeezerTrackPreview]]:
        return await self._get_engine(engine).search_tracks(query)

    async def search_albums(self, engine: Engine, query: str) -> Union[list[DeezerAlbum]]:
        return await self._get_engine(engine).search_albums(query)

    async def search_playlists(self, engine: Engine, query: str) -> Union[list[DeezerPlaylist]]:
        return await self._get_engine(engine).search_playlists(query)

    async def search_artists(self, engine: Engine, query: str) -> Union[list[DeezerArtist]]:
        return await self._get_engine(engine).search_artists(query)

    async def get_album_tracks(self, engine: Engine, album_id: int):
        return await self._get_engine(engine).get_album_tracks(album_id)

    async def get_artist_tracks(self, engine: Engine, artist_id: int):
        return await self._get_engine(engine).get_artist_tracks(artist_id)

    async def get_playlist_tracks(self, engine: Engine, playlist_id: int):
        return await self._get_engine(engine).get_playlist_tracks(playlist_id)

    async def download_track(self, engine: Engine, track_id: int) -> Union[DeezerTrack]:
        return await self._get_engine(engine).download_track(track_id)