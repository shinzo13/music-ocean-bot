import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dishka.integrations.aiogram import setup_dishka

from app.config.log import setup_logging, get_logger
from app.config.settings import settings
from app.di.container import setup_container
from app.bot.handlers.inline import default_search, chosen
from app.bot.handlers.messages import channel

setup_logging(
    level=settings.logging.level,
    log_file=settings.logging.file
)

logger = get_logger(__name__)

async def main():
    bot = Bot(
        token=settings.bot.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    container = setup_container()
    setup_dishka(container=container, router=dp, auto_inject=True)

    dp.include_routers(
        default_search.router,
        chosen.router,
        #channel.router,
    )

    try:
        await dp.start_polling(bot)
    finally:
        await container.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())