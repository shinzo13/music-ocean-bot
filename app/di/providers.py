from typing import AsyncIterator
from dishka import Provider, Scope, provide
from app.modules.musicocean import MusicOceanClient
from app.modules.musicocean_tg import TelegramMusicOceanClient
from app.config.settings import Settings, settings


class TelegramMusicOceanClientProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_deezer_client(self) -> AsyncIterator[TelegramMusicOceanClient]:
        musicocean = TelegramMusicOceanClient(
            channel_id=settings.telegram.channel_id,
            bot_token=settings.bot.token.get_secret_value()
        )

        await musicocean.setup_deezer(
            login=settings.deezer.login.get_secret_value(),
            password=settings.deezer.password.get_secret_value()
        )

        await musicocean.checkup()

        yield musicocean

        #await client.close()


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_settings(self) -> Settings:
        return settings