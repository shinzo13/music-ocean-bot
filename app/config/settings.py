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


settings = Settings()  # noqa
