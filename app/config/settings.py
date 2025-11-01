from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.types import SecretStr


class BotSettings(BaseSettings):
    token: SecretStr


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

    bot: BotSettings
    deezer: DeezerSettings


settings = Settings()  # noqa