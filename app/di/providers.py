from typing import AsyncIterator
from dishka import Provider, Scope, provide
from app.modules.musicocean_tg import TelegramMusicOceanClient
from app.config.settings import Settings, settings
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from app.database.core import create_engine, create_session_factory
from app.database.repositories import UserRepository, TrackRepository


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


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_engine(self) -> AsyncEngine:
        return create_engine(settings.database.url)

    @provide(scope=Scope.APP)
    def get_session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_session_factory(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, factory: async_sessionmaker[AsyncSession]) -> AsyncIterator[AsyncSession]:
        async with factory() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def get_user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_track_repository(self, session: AsyncSession) -> TrackRepository:
        return TrackRepository(session)