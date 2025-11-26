from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.types import SecretStr


class LoggingSettings(BaseSettings):
    level: str
    file: str

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

    logging: LoggingSettings
    bot: BotSettings
    deezer: DeezerSettings
    telegram: TelegramSettings


settings = Settings()  # noqa
