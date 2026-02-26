from typing import Optional

from app.modules.musicocean.engines import DeezerClient
from app.modules.musicocean.engines.deezer.models import (
    DeezerTrackPreview,
    DeezerTrack,
    DeezerAlbum,
    DeezerArtist,
    DeezerPlaylist
)
from app.modules.musicocean.engines.soundcloud import SoundCloudClient
from app.modules.musicocean.engines.soundcloud.models import SoundCloudTrack, SoundCloudTrackPreview, SoundCloudAlbum, \
    SoundCloudPlaylist, SoundCloudArtist
from app.modules.musicocean.engines.spotify.client import SpotifyClient
from app.modules.musicocean.engines.spotify.models import SpotifyTrackPreview
from app.modules.musicocean.engines.youtube.client import YoutubeClient
from app.modules.musicocean.enums.engine import Engine


class MusicOceanClient:
    def __init__(self, watermark: Optional[str] = None):

        self.watermark = watermark

        # TODO as fields
        self.ready = False

        self.deezer = None
        self.soundcloud = None
        self.youtube = None
        self.spotify = None

    async def setup_deezer(self, login: str, password: str) -> None:
        self.deezer = DeezerClient(
            login=login,
            password=password
        )
        await self.deezer.setup()

    async def setup_soundcloud(self) -> None:
        self.soundcloud = SoundCloudClient()
        await self.soundcloud.setup()

    async def setup_youtube(self) -> None:
        self.youtube = YoutubeClient()
        await self.youtube.setup()

    async def setup_spotify(self, client_id: str, client_secret: str) -> None:
        if not self.youtube:
            raise "setup yt first"
        self.spotify = SpotifyClient(
            client_id=client_id,
            client_secret=client_secret,
            yt=self.youtube
        )
        await self.spotify.setup()

    def _get_engine(self, engine: Engine):
        match engine:
            case Engine.DEEZER:
                select_engine = self.deezer
            case Engine.SOUNDCLOUD:
                select_engine = self.soundcloud
            case Engine.YOUTUBE:
                select_engine = self.youtube
            case Engine.SPOTIFY:
                select_engine = self.spotify
            case _:
                select_engine = None
        if not select_engine:
            raise "engine is not setup blablabla"  # TODO
        return select_engine

    async def search_tracks(
            self,
            engine: Engine,
            query: str
    ) -> list[DeezerTrackPreview] | list[SoundCloudTrackPreview]:
        return await self._get_engine(engine).search_tracks(query)

    async def search_albums(
            self, engine: Engine,
            query: str
    ) -> list[DeezerAlbum] | list[SoundCloudAlbum]:
        return await self._get_engine(engine).search_albums(query)

    async def search_playlists(
            self,
            engine: Engine,
            query: str
    ) -> list[DeezerPlaylist] | list[SoundCloudPlaylist]:
        return await self._get_engine(engine).search_playlists(query)

    async def search_artists(
            self,
            engine: Engine,
            query: str
    ) -> list[DeezerArtist] | list[SoundCloudArtist]:
        return await self._get_engine(engine).search_artists(query)

    async def get_album(self, engine: Engine, album_id: int) -> DeezerAlbum | SoundCloudAlbum:
        return await self._get_engine(engine).get_album(album_id)

    async def get_album_tracks(
            self,
            engine: Engine,
            album_id: int
    ) -> list[DeezerTrackPreview] | list[SoundCloudTrackPreview]:
        return await self._get_engine(engine).get_album_tracks(album_id)

    async def get_artist(self, engine: Engine, artist_id: int) -> DeezerArtist | SoundCloudArtist:
        return await self._get_engine(engine).get_artist(artist_id)

    async def get_artist_tracks(
            self,
            engine: Engine,
            artist_id: int
    ) -> list[DeezerTrackPreview] | list[SoundCloudTrackPreview]:
        return await self._get_engine(engine).get_artist_tracks(artist_id)

    async def get_playlist(self, engine: Engine, playlist_id: int) -> DeezerPlaylist | SoundCloudPlaylist:
        return await self._get_engine(engine).get_artist(playlist_id)

    async def get_playlist_tracks(
            self,
            engine: Engine,
            playlist_id: int
    ) -> list[DeezerTrackPreview] | list[SoundCloudTrackPreview]:
        return await self._get_engine(engine).get_playlist_tracks(playlist_id)

    async def download_track(
            self,
            engine: Engine,
            track_id: int
    ) -> DeezerTrack | SoundCloudTrack:
        return await self._get_engine(engine).download_track(track_id, self.watermark)

    async def exchange_spotify_code(self, code: str, redirect_uri: str) -> dict:
        if not self.spotify:
            raise "spotify is not setup"
        return await self.spotify.exchange_code(code, redirect_uri)

    async def refresh_spotify_user_token(self, refresh_token: str) -> str:
        if not self.spotify:
            raise "spotify is not setup"
        return await self.spotify.refresh_token(refresh_token)

    async def get_spotify_last_track(
            self,
            access_token: str,
            refresh_token: str
    ) -> SpotifyTrackPreview | None:
        if not self.spotify:
            raise "spotify is not setup"
        return await self.spotify.get_last_track(access_token, refresh_token)

    async def get_spotify_recently_played(
            self,
            access_token: str,
            refresh_token: str
    ) -> list[SpotifyTrackPreview]:
        if not self.spotify:
            raise "spotify is not setup"
        return await self.spotify.get_recently_played(access_token, refresh_token)