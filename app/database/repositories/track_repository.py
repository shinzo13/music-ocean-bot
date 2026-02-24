from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.log import get_logger
from app.database.models.base_track import BaseTrack
from app.database.models.deezer_track import DeezerTrack
from app.database.models.soundcloud_track import SoundCloudTrack
from app.database.models.spotify_track import SpotifyTrack
from app.database.models.youtube_track import YoutubeTrack
from app.modules.musicocean.enums.engine import Engine

logger = get_logger(__name__)


class TrackRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_track(
            self,
            engine: Engine,
            track_id: int | str,
            telegram_file_id: str,
            user_id: int
    ) -> DeezerTrack | SoundCloudTrack | YoutubeTrack | SpotifyTrack:
        kwargs = {
            'track_id': track_id,
            'telegram_file_id': telegram_file_id,
            'user_id': user_id
        }
        match engine:
            case Engine.DEEZER:
                track = DeezerTrack(**kwargs)
            case Engine.SOUNDCLOUD:
                track = SoundCloudTrack(**kwargs)
            case Engine.YOUTUBE:
                track = YoutubeTrack(**kwargs)
            case Engine.SPOTIFY:
                track = SpotifyTrack(**kwargs)
            case _:
                raise

        self.session.add(track)
        await self.session.commit()
        await self.session.refresh(track)
        logger.debug(f"Added track: {track}")
        return track

    async def get_track(
            self,
            track_id: int | str,
            engine: Engine
    ) -> Optional[DeezerTrack | SoundCloudTrack | YoutubeTrack | SpotifyTrack]:
        match engine:
            case Engine.DEEZER:
                target = DeezerTrack
            case Engine.SOUNDCLOUD:
                target = SoundCloudTrack
            case Engine.YOUTUBE:
                target = YoutubeTrack
            case Engine.SPOTIFY:
                target = SpotifyTrack
            case _:
                raise

        result = await self.session.execute(
            select(target).where(
                target.track_id == track_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_track_by_file_id(
            self,
            file_id: str
    ) -> Optional[DeezerTrack | SoundCloudTrack | YoutubeTrack | SpotifyTrack]:
        result = await self.session.execute(
            select(BaseTrack).where(BaseTrack.telegram_file_id == file_id)
        )
        return result.scalar_one_or_none()
