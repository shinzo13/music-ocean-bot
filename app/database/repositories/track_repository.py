from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Track
from app.modules.musicocean.enums.engine import Engine
from app.config.log import get_logger

logger = get_logger(__name__)

class TrackRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_track(
        self,
        engine: Engine,
        track_id: int,
        telegram_file_id: str,
        user_id: int
    ) -> Track:
        track = Track(
            engine=engine,
            track_id=track_id,
            telegram_file_id=telegram_file_id,
            user_id=user_id
        )
        self.session.add(track)
        await self.session.commit()
        await self.session.refresh(track)
        logger.debug(f"Added track: {track}")
        return track

    async def get_track_by_id(self, track_id: int) -> Optional[Track]:
        result = await self.session.execute(
            select(Track).where(Track.track_id == track_id)
        )
        return result.scalar_one_or_none()