import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dishka.integrations.aiogram import setup_dishka

from app.bot.handlers.inline import (
    default_search,
    chosen,
    advanced_search,
    id_search
)
from app.bot.middlewares import MainMiddleware
from app.config.log import setup_logging, get_logger
from app.config.settings import settings
from app.database.core import create_engine
from app.database.models.base import Base
from app.di.container import setup_container

setup_logging(level=settings.logging.level)
logger = get_logger(__name__)


async def main():
    bot = Bot(
        token=settings.bot.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    engine = create_engine(settings.database.url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    container = setup_container()
    setup_dishka(container=container, router=dp, auto_inject=True)

    dp.update.outer_middleware(MainMiddleware())

    dp.include_routers(
        id_search.router,
        advanced_search.router,
        default_search.router,
        chosen.router,
        # channel.router,
    )

    try:
        await dp.start_polling(bot)
    finally:
        await container.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
