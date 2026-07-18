from typing import Optional

from sqlalchemy import select, or_, func, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import with_polymorphic

from app.config.log import get_logger
from app.database.models.base_track import BaseTrack
from app.database.models.download_context import DownloadContext, EntityType, DownloadMode
from app.database.models.deezer_track import DeezerTrack
from app.database.models.soundcloud_track import SoundCloudTrack
from app.database.models.spotify_track import SpotifyTrack
from app.database.models.yandex_track import YandexTrack
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
            user_id: int,
            telegram_file_unique_id: str | None = None,
            download_context: DownloadContext = DownloadContext.SEARCH,
            entity_type: EntityType | None = None,
            download_mode: DownloadMode | None = None
    ) -> DeezerTrack | SoundCloudTrack | YoutubeTrack | SpotifyTrack:
        kwargs = {
            'track_id': track_id,
            'telegram_file_id': telegram_file_id,
            'telegram_file_unique_id': telegram_file_unique_id,
            'user_id': user_id,
            'download_context': download_context,
            'entity_type': entity_type,
            'download_mode': download_mode
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
            case Engine.YANDEX:
                track = YandexTrack(**kwargs)
            case _:
                raise

        self.session.add(track)
        await self.session.commit()
        await self.session.refresh(track)
        logger.debug(f"Added track: {track}")
        return track

    async def update_file(
            self,
            track_id: int | str,
            engine: Engine,
            telegram_file_id: str,
            telegram_file_unique_id: str | None = None
    ) -> None:
        track = await self.get_track(track_id, engine)
        if track is None:
            return
        track.telegram_file_id = telegram_file_id
        track.telegram_file_unique_id = telegram_file_unique_id
        await self.session.commit()

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
            case Engine.YANDEX:
                target = YandexTrack
            case _:
                raise

        result = await self.session.execute(
            select(target).where(
                target.track_id == track_id,
            )
        )
        return result.scalar_one_or_none()

    async def usage_stats(self) -> dict:
        total = (await self.session.execute(
            select(func.count()).select_from(BaseTrack)
        )).scalar_one()
        users = (await self.session.execute(
            select(func.count(distinct(BaseTrack.user_id)))
        )).scalar_one()
        by_context = (await self.session.execute(
            select(BaseTrack.download_context, func.count())
            .group_by(BaseTrack.download_context)
        )).all()
        by_entity = (await self.session.execute(
            select(BaseTrack.entity_type, BaseTrack.download_mode, func.count())
            .where(BaseTrack.download_context == DownloadContext.ENTITY)
            .group_by(BaseTrack.entity_type, BaseTrack.download_mode)
        )).all()
        by_engine = (await self.session.execute(
            select(BaseTrack.engine, func.count())
            .group_by(BaseTrack.engine)
        )).all()
        return {
            'total': total,
            'users': users,
            'by_context': dict(by_context),
            'by_entity': {(e, m): c for e, m, c in by_entity},
            'by_engine': dict(by_engine),
        }

    async def get_track_by_file(
            self,
            file_unique_id: str,
            file_id: str
    ) -> Optional[DeezerTrack | SoundCloudTrack | YoutubeTrack | SpotifyTrack]:
        # file_id is unstable across delivery contexts; match on the stable
        # file_unique_id first, fall back to file_id for legacy rows
        wp = with_polymorphic(BaseTrack, "*")
        result = await self.session.execute(
            select(wp)
            .where(or_(
                BaseTrack.telegram_file_unique_id == file_unique_id,
                BaseTrack.telegram_file_id == file_id
            ))
        )
        return result.scalars().first()
