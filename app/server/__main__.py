import asyncio

from aiohttp import web
from dishka.integrations.aiohttp import setup_dishka

from app.config.log import setup_logging, get_logger
from app.config.settings import settings
from app.database.core import create_engine
from app.database.models.base import Base
from app.di.container import setup_container
from app.server.callback_endpoint import app, ssl_context

setup_logging(level=settings.logging.level)
logger = get_logger(__name__)


async def main():
    engine = create_engine(settings.database.url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    container = setup_container()
    setup_dishka(container=container, app=app, auto_inject=True)

    runner = web.AppRunner(app)
    try:
        await runner.setup()
        await web.TCPSite(runner, "0.0.0.0", 443, ssl_context=ssl_context).start()
        logger.info("Callback server started on :443")
        await asyncio.Event().wait()
    finally:
        await container.close()
        await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())