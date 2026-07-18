import asyncio
from typing import Optional

from yandex_music import ClientAsync

from app.config.log import get_logger
from app.modules.musicocean.engines.shared.base_client import BaseEngineClient
from app.modules.musicocean.engines.yandex.constants import (
    COVER_SIZE,
    DEFAULT_BITRATE,
    DEFAULT_CODEC,
)
from app.modules.musicocean.engines.yandex.exceptions import YandexDataException
from app.modules.musicocean.engines.yandex.models import (
    YandexAlbum,
    YandexArtist,
    YandexPlaylist,
    YandexTrack,
    YandexTrackPreview,
)
from app.modules.musicocean.utils.id3 import write_mp3_tags

logger = get_logger(__name__)

ARTIST_TRACKS_PAGE_SIZE = 50


class YandexClient(BaseEngineClient):
    def __init__(
            self,
            token: str,
            codec: str = DEFAULT_CODEC,
            bitrate_in_kbps: int = DEFAULT_BITRATE,
    ):
        self.token = token
        self.codec = codec
        self.bitrate_in_kbps = bitrate_in_kbps
        self.client: Optional[ClientAsync] = None

    async def setup(self):
        self.client = await ClientAsync(self.token).init()

    @staticmethod
    def _parse_playlist_id(playlist_id: int | str) -> tuple[str, str]:
        try:
            uid, kind = str(playlist_id).split(":", maxsplit=1)
        except ValueError:
            raise YandexDataException(f"Invalid Yandex playlist id: {playlist_id}")
        return uid, kind

    async def get_track(self, track_id: int | str) -> YandexTrackPreview:
        tracks = await self.client.tracks([track_id])
        if not tracks:
            raise YandexDataException("Track not found")
        return YandexTrackPreview.from_obj(tracks[0])

    async def search_tracks(self, query: str) -> list[YandexTrackPreview]:
        result = await self.client.search(query, type_="track")
        if not result or not result.tracks:
            return []
        return [YandexTrackPreview.from_obj(t) for t in result.tracks.results]

    async def search_albums(self, query: str) -> list[YandexAlbum]:
        result = await self.client.search(query, type_="album")
        if not result or not result.albums:
            return []
        return [YandexAlbum.from_obj(a) for a in result.albums.results]

    async def search_playlists(self, query: str) -> list[YandexPlaylist]:
        result = await self.client.search(query, type_="playlist")
        if not result or not result.playlists:
            return []
        return [YandexPlaylist.from_obj(p) for p in result.playlists.results]

    async def search_artists(self, query: str) -> list[YandexArtist]:
        result = await self.client.search(query, type_="artist")
        if not result or not result.artists:
            return []
        return [YandexArtist.from_obj(a) for a in result.artists.results]

    async def get_album(self, album_id: int | str) -> YandexAlbum:
        album = await self.client.albums_with_tracks(album_id)
        if not album:
            raise YandexDataException("Album not found")
        return YandexAlbum.from_obj(album)

    async def get_album_tracks(self, album_id: int | str) -> list[YandexTrackPreview]:
        album = await self.client.albums_with_tracks(album_id)
        if not album or not album.volumes:
            raise YandexDataException("Album not found")
        return [
            YandexTrackPreview.from_obj(track)
            for volume in album.volumes
            for track in volume
        ]

    async def get_artist(self, artist_id: int | str) -> YandexArtist:
        artists = await self.client.artists([artist_id])
        if not artists:
            raise YandexDataException("Artist not found")
        return YandexArtist.from_obj(artists[0])

    async def get_artist_tracks(self, artist_id: int | str) -> list[YandexTrackPreview]:
        artist_tracks = await self.client.artists_tracks(
            artist_id,
            page_size=ARTIST_TRACKS_PAGE_SIZE,
        )
        if not artist_tracks:
            raise YandexDataException("Artist not found")
        return [YandexTrackPreview.from_obj(t) for t in artist_tracks.tracks]

    async def get_playlist(self, playlist_id: int | str) -> YandexPlaylist:
        uid, kind = self._parse_playlist_id(playlist_id)
        playlist = await self.client.users_playlists(kind, user_id=uid)
        if not playlist:
            raise YandexDataException("Playlist not found")
        return YandexPlaylist.from_obj(playlist)

    async def get_playlist_tracks(self, playlist_id: int | str) -> list[YandexTrackPreview]:
        uid, kind = self._parse_playlist_id(playlist_id)
        playlist = await self.client.users_playlists(kind, user_id=uid)
        if not playlist:
            raise YandexDataException("Playlist not found")
        track_ids = [ts.track_id for ts in playlist.tracks]
        if not track_ids:
            return []
        tracks = await self.client.tracks(track_ids)
        return [YandexTrackPreview.from_obj(t) for t in tracks]

    async def download_track(
            self,
            track_id: int | str,
            watermark: Optional[str] = None
    ) -> YandexTrack:
        tracks = await self.client.tracks([track_id])
        if not tracks:
            raise YandexDataException("Track not found")
        raw_track = tracks[0]

        # lossless: branch on codec == "flac" via get_download_info_async()
        source = await raw_track.download_bytes_async(
            codec=self.codec,
            bitrate_in_kbps=self.bitrate_in_kbps,
        )

        track = YandexTrack.from_obj(raw_track)
        if track.cover_url:
            track.cover = await raw_track.download_cover_bytes_async(size=COVER_SIZE)

        track.content = await asyncio.to_thread(
            write_mp3_tags,
            track=track,
            source=source,
            watermark=watermark,
        )
        return track

    async def close(self):
        pass
