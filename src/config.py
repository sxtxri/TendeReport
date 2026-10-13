import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        case_sensitive=False,
        env_file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            ".env",
        ),
    )


class ServerSettings(ConfigSettings):
    port: int = 8080
    host: str = "127.0.0.1"
    model_config = SettingsConfigDict(env_prefix="SERVER_")


class Settings(ConfigSettings):
    SERVICE_NAME: str
    ENV: str = Field("local", alias="ENVIRONMENT")
    DEBUG: bool
    BASE_DIR: Path = Path(__file__).resolve().parent
    IS_ENABLED_METRICS: bool = False

    # Настройки сервера
    server: ServerSettings = Field(default_factory=ServerSettings)


settings = Settings()
