from abc import ABC, abstractmethod
from typing import Optional

from app.modules.musicocean.engines.shared.models import BaseTrackPreview, BaseAlbum, BasePlaylist, BaseArtist, \
    BaseTrack


class BaseEngineClient(ABC):

    @abstractmethod
    async def setup(self):
        pass

    @abstractmethod
    async def search_tracks(self, query: str) -> list[BaseTrackPreview]:
        pass

    @abstractmethod
    async def search_albums(self, query: str) -> list[BaseAlbum]:
        pass

    @abstractmethod
    async def search_playlists(self, query: str) -> list[BasePlaylist]:
        pass

    @abstractmethod
    async def search_artists(self, query: str) -> list[BaseArtist]:
        pass

    @abstractmethod
    async def get_album(self, album_id: int):
        pass

    @abstractmethod
    async def get_playlist(self, playlist_id: int):
        pass
    @abstractmethod
    async def get_album_tracks(self, album_id: int):
        pass

    @abstractmethod
    async def get_artist(self, artist_id: int):
        pass

    @abstractmethod
    async def get_artist_tracks(self, artist_id: int):
        pass

    @abstractmethod
    async def get_playlist_tracks(self, playlist_id: int):
        pass

    @abstractmethod
    async def download_track(
            self,
            track_id: int,
            watermark: Optional[str] = None
    ) -> BaseTrack:
        pass


    @abstractmethod
    async def close(self):
        pass

