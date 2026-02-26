import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import web
from dishka.integrations.aiogram import setup_dishka as setup_dishka_aiogram
from dishka.integrations.aiohttp import setup_dishka as setup_dishka_aiohttp

from app.bot.handlers import (
    inline_search,
    process_track,
    user_interface,
    track_info,
    admin_panel
)
from app.bot.middlewares import MainMiddleware
from app.config.log import setup_logging, get_logger
from app.config.settings import settings
from app.database.core import create_engine, add_env_admins
from app.database.models.base import Base
from app.di.container import setup_container
from app.server.callback_endpoint import app

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
    await add_env_admins(engine, settings.telegram.admins)

    container = setup_container()
    setup_dishka_aiogram(container=container, router=dp, auto_inject=True)
    setup_dishka_aiohttp(container=container, app=app, auto_inject=True)

    dp.update.outer_middleware(MainMiddleware())

    dp.include_routers(
        *inline_search.routers,
        *process_track.routers,
        *user_interface.routers,
        *track_info.routers,
        *admin_panel.routers
    )

    runner = web.AppRunner(app)

    try:
        await runner.setup()
        await web.TCPSite(runner, "0.0.0.0", 8080).start()
        await dp.start_polling(bot)
    finally:
        await container.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
