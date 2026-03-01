from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.log import get_logger
from app.database.models import DynamicSettings

logger = get_logger(__name__)


class DynamicSettingsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self) -> Optional[DynamicSettings]:
        result = await self.session.execute(select(DynamicSettings))
        return result.scalar_one_or_none()

    async def update(self, **kwargs) -> DynamicSettings:
        config = await self.get()
        if config is None:
            config = DynamicSettings(**kwargs)
            self.session.add(config)
        else:
            for key, value in kwargs.items():
                try:
                    setattr(config, key, value)
                except KeyError:
                    raise # todo

        await self.session.commit()
        await self.session.refresh(config)
        logger.info(f"Updated dynamic config: {kwargs}")
        return config