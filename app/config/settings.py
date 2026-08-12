from typing import List, Optional

from pydantic.types import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DevSettings(BaseSettings):
    enabled: bool
    arl: str
    client_id: str


class LoggingSettings(BaseSettings):
    level: str


class DatabaseSettings(BaseSettings):
    user: str
    password: SecretStr
    db: str
    host: str = "postgres"
    port: int = 5432

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"



class BotSettings(BaseSettings):
    token: SecretStr


class ServerSettings(BaseSettings):
    domain: str
    certfile_path: str
    keyfile_path: str


class TelegramSettings(BaseSettings):
    admins: list[int]
    channel_id: int
    workers: List[SecretStr]


class DeezerSettings(BaseSettings):
    login: SecretStr
    password: SecretStr


class SpotifySettings(BaseSettings):
    client_id: SecretStr
    client_secret: SecretStr


class YandexSettings(BaseSettings):
    token: SecretStr
    proxy: Optional[SecretStr] = None

class LastfmSettings(BaseSettings):
    api_key: SecretStr

class LocalSettings(BaseSettings):
    watermark: Optional[str]
    guide_url: Optional[str]
    # public project name is "Music Ocean"; a deployment can rebrand the
    # user-facing name via LOCAL__BRAND without touching the repo
    brand: str = "Music Ocean"

class EnginesSettings(BaseSettings):
    # engines listed here stay in the codebase but are hidden from users and
    # never set up on boot, e.g. ENGINES__DISABLED=["YANDEX"]
    disabled: List[str] = []

    def is_enabled(self, engine) -> bool:
        return str(getattr(engine, "value", engine)).upper() not in {e.upper() for e in self.disabled}


class LimitsSettings(BaseSettings):
    # a batch downloads every track into memory, so an unbounded album or a
    # handful of parallel playlists is all it takes to knock the bot over
    max_entity_tracks: int = 100
    batch_concurrency: int = 4
    max_concurrent_batches: int = 3


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter='__',
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False
    )

    dev: DevSettings

    logging: LoggingSettings
    bot: BotSettings
    server: ServerSettings
    telegram: TelegramSettings
    deezer: DeezerSettings
    spotify: SpotifySettings
    yandex: YandexSettings
    lastfm: LastfmSettings
    database: DatabaseSettings
    local: LocalSettings
    limits: LimitsSettings = LimitsSettings()
    engines: EnginesSettings = EnginesSettings()


settings = Settings()  # noqa
