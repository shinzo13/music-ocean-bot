from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User
from app.config.log import get_logger
from app.modules.musicocean.enums import Engine

logger = get_logger(__name__)

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self,user_id: int) -> User:
        user = User(
            user_id=user_id,
            is_admin=False,
            is_banned=False,
            selected_engine=Engine.DEEZER
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
            setattr(user, key, value)

        await self.session.commit()
        await self.session.refresh(user)
        logger.info(f"Updated user: {user}")
        return user

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.user_id == user_id)
        )
        return result.scalar_one_or_none()