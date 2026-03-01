import csv
import io
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, attributes
from sqlalchemy.orm.attributes import flag_modified

from app.config.log import get_logger
from app.database.models import User
from app.database.models.user import UserSettings
from app.modules.musicocean.enums.engine import Engine

logger = get_logger(__name__)


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, user_id: int) -> User:
        user = User(
            user_id=user_id,
            is_admin=False,
            is_banned=False,
            settings=UserSettings()
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        logger.info(f"Added user: {user}")
        return user

    async def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        user = await self.get_user_by_id(user_id)
        if user is None:
            return None

        for key, value in kwargs.items():
            if key == "settings":
                raise "for changing settings field use update_user_settings instead"
            setattr(user, key, value)

        await self.session.commit()
        await self.session.refresh(user)
        logger.info(f"Updated user: {user}")
        return user

    async def update_user_settings(
            self,
            user_id: int,
            selected_engine: Optional[Engine] = None,
            track_preview_covers: Optional[bool] = None,
            spotify__enabled: Optional[bool] = None,
            spotify__connection_code: Optional[str] = None,
            spotify__access_token: Optional[str] = None,
            spotify__refresh_token: Optional[str] = None,
    ) -> Optional[User]:
        user = await self.get_user_by_id(user_id)
        if user is None:
            return None

        if selected_engine is not None:
            user.settings.selected_engine = selected_engine
        if track_preview_covers is not None:
            user.settings.track_preview_covers = track_preview_covers
        if spotify__enabled is not None:
            user.settings.spotify.enabled = spotify__enabled
        if spotify__connection_code is not None:
            user.settings.spotify.connection_code = spotify__connection_code
        if spotify__access_token is not None:
            user.settings.spotify.access_token = spotify__access_token
        if spotify__refresh_token is not None:
            user.settings.spotify.refresh_token = spotify__refresh_token

        flag_modified(user, 'settings')
        await self.session.commit()
        await self.session.refresh(user)
        logger.info(f"Updated settings for user {user_id}")
        return user

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_user_downloaded_tracks(self, user_id: int):
        result = await self.session.execute(
            select(User)
            .options(selectinload(User.downloaded_tracks))
            .where(User.user_id == user_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            return []

        return user.downloaded_tracks

    async def export_to_csv(self) -> bytes:
        result = await self.session.execute(select(User))
        users = result.scalars().all()
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow([
            'user_id',
            'is_admin',
            'is_banned',
            'selected_engine',
            'track_preview_covers'
        ])

        for user in users:
            writer.writerow([
                user.user_id,
                user.is_admin,
                user.is_banned,
                user.settings.selected_engine.value,
                user.settings.track_preview_covers
            ])

        csv_bytes = output.getvalue().encode('utf-8')
        output.close()

        return csv_bytes