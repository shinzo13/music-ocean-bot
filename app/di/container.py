from dishka import make_async_container, AsyncContainer

from app.di.providers import TelegramMusicOceanClientProvider, DatabaseProvider


def setup_container() -> AsyncContainer:
    container = make_async_container(
        TelegramMusicOceanClientProvider(),
        DatabaseProvider()
    )
    return container
