from typing import List

from pydantic.types import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DevSettings(BaseSettings):
    enabled: bool
    arl: str


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


class TelegramSettings(BaseSettings):
    channel_id: int
    workers: List[SecretStr]


class DeezerSettings(BaseSettings):
    login: SecretStr
    password: SecretStr


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
    telegram: TelegramSettings
    deezer: DeezerSettings
    database: DatabaseSettings


settings = Settings()  # noqa
