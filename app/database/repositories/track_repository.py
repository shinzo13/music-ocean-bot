from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Track


class TrackRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # TODO kwargs to typesafe
    async def add_track(self, **kwargs) -> Track:
        track = Track(**kwargs)
        self.session.add(track)
        await self.session.commit()
        await self.session.refresh(track)
        return track

    async def get_track_by_id(self, track_id: int) -> Optional[Track]:
        result = await self.session.execute(
            select(Track).where(Track.id == track_id)
        )
        return result.scalar_one_or_none()