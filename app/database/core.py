from typing import Any

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy import select, update

from app.database.models import User
from app.config.log import get_logger
from app.database.models.user import UserSettings
from app.database.repositories import UserRepository, DynamicSettingsRepository

logger = get_logger(__name__)

def create_engine(database_url: str) -> AsyncEngine:
    return create_async_engine(database_url)


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)

async def initialize_dynamic_settings(engine: AsyncEngine, **kwargs: Any) -> None:
    factory = create_session_factory(engine)
    async with factory() as session:
        await DynamicSettingsRepository(session).update(**kwargs)
        await session.commit()

async def add_env_admins(engine: AsyncEngine, env_admins: list[int]):
    factory = create_session_factory(engine)
    async with factory() as session:
        user_repo = UserRepository(session)
        for user_id in env_admins:
            user = await user_repo.get_user_by_id(user_id)
            if user is None:
                user = await user_repo.add_user(user_id=user_id)
                user.is_admin = True
                logger.info(f"Created admin user: #{user_id}")
            elif not user.is_admin:
                user.is_admin = True
                logger.info(f"Updated user #{user_id} to admin")
        await session.commit()
