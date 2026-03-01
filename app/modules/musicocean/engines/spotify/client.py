import base64
import time
from typing import Optional
from datetime import datetime, timedelta, timezone

from aiohttp import ClientSession

from app.config.log import get_logger
from app.modules.musicocean.engines.spotify.constants import (
    SPOTIFY_API_BASE,
    SPOTIFY_TOKEN_URL
)
from app.modules.musicocean.engines.spotify.enums import SpotifySearchType
from app.modules.musicocean.engines.spotify.exceptions import (
    SpotifyAuthException,
    SpotifyDataException,
    SpotifyException,
)
from app.modules.musicocean.engines.spotify.models import (
    SpotifyAlbum,
    SpotifyArtist,
    SpotifyPlaylist,
    SpotifyTrackPreview,
)
from app.modules.musicocean.engines.youtube.client import YoutubeClient
from app.modules.musicocean.engines.youtube.models.youtube_track import YoutubeTrack

logger = get_logger(__name__)


class SpotifyClient:

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        yt: YoutubeClient,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.yt = yt

        self.session: Optional[ClientSession] = None
        self._access_token: Optional[str] = None
        self._token_expires_at: float = 0.0

    async def setup(self):
        self.session = ClientSession(raise_for_status=False)
        await self._refresh_token()

    async def close(self):
        if self.session:
            await self.session.close()

    async def _refresh_token(self):
        credentials = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()

        async with self.session.post(
            SPOTIFY_TOKEN_URL,
            headers={
                "Authorization": f"Basic {credentials}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={"grant_type": "client_credentials"},
        ) as resp:
            data = await resp.json()

        if "access_token" not in data:
            raise SpotifyAuthException(
                f"Failed to obtain access token: {data.get('error_description', data)}"
            )

        self._access_token = data["access_token"]
        self._token_expires_at = time.monotonic() + data.get("expires_in", 3600) - 60
        logger.info("Spotify access token refreshed.")

    async def _ensure_token(self):
        if time.monotonic() >= self._token_expires_at:
            await self._refresh_token()

    @property
    def _auth_headers(self) -> dict:
        return {"Authorization": f"Bearer {self._access_token}"}


    async def exchange_code(self, code: str, redirect_uri: str) -> tuple[str, str]:
        credentials = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()

        async with self.session.post(
            SPOTIFY_TOKEN_URL,
            headers={
                "Authorization": f"Basic {credentials}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
            },
        ) as resp:
            data = await resp.json()
            logger.debug(f"Spotify exchange response: {data}")

        return data["access_token"], data["refresh_token"]

    async def refresh_user_token(self, refresh_token: str) -> str:
        credentials = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()

        async with self.session.post(
            SPOTIFY_TOKEN_URL,
            headers={
                "Authorization": f"Basic {credentials}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
        ) as resp:
            data = await resp.json()

        if "access_token" not in data:
            raise SpotifyAuthException(
                f"Failed to refresh user token: {data.get('error_description', data)}"
            )

        return data["access_token"]

    async def _get(self, path: str, **params) -> dict:
        await self._ensure_token()
        async with self.session.get(
            f"{SPOTIFY_API_BASE}/{path}",
            headers=self._auth_headers,
            params={k: v for k, v in params.items() if v is not None},
        ) as resp:
            data = await resp.json()

        if "error" in data:
            status = data["error"].get("status")
            message = data["error"].get("message", "Unknown error")
            if status == 401:
                logger.warning("Spotify token expired mid-request, refreshing...")
                await self._refresh_token()
                return await self._get(path, **params)
            if status == 404:
                raise SpotifyDataException(f"Not found: {message}")
            raise SpotifyException(f"Spotify API error {status}: {message}")

        return data

    async def _user_get(
        self,
        user_access_token: str,
        refresh_token: str,
        path: str,
        **params,
    ) -> tuple[dict | None, str]:
        async with self.session.get(
            f"{SPOTIFY_API_BASE}/{path}",
            headers={"Authorization": f"Bearer {user_access_token}"},
            params={k: v for k, v in params.items() if v is not None},
        ) as resp:
            if resp.status == 204:
                return None, user_access_token
            data = await resp.json()

        if "error" in data and data["error"].get("status") == 401:
            logger.info("Spotify user token expired, refreshing...")
            user_access_token = await self.refresh_user_token(refresh_token)
            async with self.session.get(
                f"{SPOTIFY_API_BASE}/{path}",
                headers={"Authorization": f"Bearer {user_access_token}"},
                params={k: v for k, v in params.items() if v is not None},
            ) as resp:
                if resp.status == 204:
                    return None, user_access_token
                data = await resp.json()

        return data, user_access_token

    async def _search(self, query: str, search_type: SpotifySearchType) -> list[dict]:
        data = await self._get(
            "search",
            q=query,
            type=search_type.value,
            limit=10,
        )
        return list(filter(
            lambda x: x is not None,
            data[search_type.value + 's']["items"]
        ))

    async def search_tracks(self, query: str) -> list[SpotifyTrackPreview]:
        raw = await self._search(query, SpotifySearchType.TRACK)
        return [SpotifyTrackPreview.from_dict(item) for item in raw]

    async def search_albums(self, query: str) -> list[SpotifyAlbum]:
        raw = await self._search(query, SpotifySearchType.ALBUM)
        return [SpotifyAlbum.from_dict(item) for item in raw]

    async def search_playlists(self, query: str) -> list[SpotifyPlaylist]:
        raw = await self._search(query, SpotifySearchType.PLAYLIST)
        return [SpotifyPlaylist.from_dict(item) for item in raw]

    async def search_artists(self, query: str) -> list[SpotifyArtist]:
        raw = await self._search(query, SpotifySearchType.ARTIST)
        return [SpotifyArtist.from_dict(item) for item in raw]

    async def get_track(self, track_id: str) -> SpotifyTrackPreview:
        data = await self._get(f"tracks/{track_id}")
        return SpotifyTrackPreview.from_dict(data)

    async def get_album(self, album_id: str) -> SpotifyAlbum:
        data = await self._get(f"albums/{album_id}")
        return SpotifyAlbum.from_dict(data)

    async def get_album_tracks(self, album_id: str) -> list[SpotifyTrackPreview]:
        tracks: list[SpotifyTrackPreview] = []
        path = f"/albums/{album_id}/tracks"
        album = await self.get_album(album_id)
        while path:
            path.removeprefix(f"{SPOTIFY_API_BASE}/")
            data = await self._get(path, limit=10)
            for item in data["items"]:
                item["cover_url"] = album.cover_url
                tracks.append(SpotifyTrackPreview.from_dict(item))
            if not (path := data.get("next")):
                break
        return tracks

    async def get_playlist(self, playlist_id: str) -> SpotifyPlaylist:
        data = await self._get(f"playlists/{playlist_id}")
        return SpotifyPlaylist.from_dict(data)

    async def get_playlist_tracks(self, playlist_id: str) -> list[SpotifyTrackPreview]:
        tracks: list[SpotifyTrackPreview] = []
        path = f"/playlists/{playlist_id}/tracks"
        while path:
            path.removeprefix(f"{SPOTIFY_API_BASE}/")
            data = await self._get(path, limit=10)
            for item in data["items"]:
                if item.get("track"):
                    tracks.append(SpotifyTrackPreview.from_dict(item["track"]))
            if not (path := data.get("next")):
                break
        return tracks

    async def get_artist(self, artist_id: str) -> SpotifyArtist:
        data = await self._get(f"artists/{artist_id}")
        return SpotifyArtist.from_dict(data)

    async def get_artist_tracks(self, artist_id: str) -> list[SpotifyTrackPreview]:
        data = await self._get(f"artists/{artist_id}/top-tracks", limit=10)
        return [SpotifyTrackPreview.from_dict(item) for item in data["tracks"]]

    async def get_last_track(
        self,
        user_access_token: str,
        refresh_token: str,
    ) -> tuple[SpotifyTrackPreview | None, str]:
        data, user_access_token = await self._user_get(
            user_access_token, refresh_token, "me/player/currently-playing"
        )
        if data and data.get("item") and data.get("is_playing"):
            return SpotifyTrackPreview.from_dict(data["item"]), user_access_token

        data, user_access_token = await self._user_get(
            user_access_token, refresh_token, "me/player/recently-played", limit=1
        )
        if not data or not data.get("items"):
            return None, user_access_token

        last = data["items"][0]
        played_at = datetime.fromisoformat(last["played_at"].replace("Z", "+00:00"))
        if datetime.now(timezone.utc) - played_at > timedelta(minutes=5):
            return None, user_access_token

        return SpotifyTrackPreview.from_dict(last["track"]), user_access_token

    async def get_recently_played(
        self,
        user_access_token: str,
        refresh_token: str,
    ) -> tuple[list[SpotifyTrackPreview], str]:
        data, user_access_token = await self._user_get(
            user_access_token, refresh_token, "me/player/recently-played", limit=50
        )
        if not data or not data.get("items"):
            return [], user_access_token
        return (
            [SpotifyTrackPreview.from_dict(item["track"]) for item in data["items"]],
            user_access_token,
        )

    async def download_track(
        self,
        track_id: str,
        watermark: Optional[str] = None,
    ) -> YoutubeTrack:
        track = await self.get_track(track_id)
        match = await self.yt.search_exact_match(track.title, track.artist_name)
        if not match:
            raise SpotifyException("No YouTube matches found for Spotify track")

        return await self.yt.download_track(
            match.id,
            watermark=watermark,
        )