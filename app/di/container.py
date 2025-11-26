from dishka import make_async_container, AsyncContainer
from app.di.providers import TelegramMusicOceanClientProvider, ConfigProvider


def setup_container() -> AsyncContainer:
    container = make_async_container(
        TelegramMusicOceanClientProvider(),
        ConfigProvider(),
    )
    return container