import os
from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import Field, PostgresDsn, field_validator
from pydantic_core.core_schema import ValidationInfo
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


class ScrapperSettings(ConfigSettings):
    USER_AGENT: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )


class NotificationClientType(StrEnum):

    FAKE = "fake"
    VK = "vk"


class NotificationSettings(ConfigSettings):
    CLIENT: NotificationClientType = NotificationClientType.FAKE
    VK_TOKEN: str = ""
    VK_PEER_ID: str = ""
    VK_API_VERSION: str = "5.199"
    model_config = SettingsConfigDict(env_prefix="NOTIFICATION_")


class Settings(ConfigSettings):
    SERVICE_NAME: str
    ENV: str = Field("local", alias="ENVIRONMENT")
    DEBUG: bool
    BASE_DIR: Path = Path(__file__).resolve().parent
    IS_ENABLED_METRICS: bool = False

    # Postgres credentials
    POSTGRES_DB_NAME: str
    POSTGRES_DB_USER: str
    POSTGRES_DB_PASSWORD: str
    POSTGRES_DB_HOST: str
    POSTGRES_DB_PORT: int
    POSTGRES_POOL_MIN_SIZE: int = 1
    POSTGRES_POOL_MAX_SIZE: int = 3
    POSTGRES_DSN: str | None = None

    # test
    POSTGRES_TEST_DB_NAME: str | None = None
    POSTGRES_TEST_DSN: str | None = None
    APPLY_MIGRATIONS_FOR_TESTS: bool = True

    # Notification settings
    NOTIFICATION_CLIENT: NotificationClientType = NotificationClientType.FAKE
    VK_TOKEN: str = ""
    VK_PEER_ID: str = ""
    VK_API_VERSION: str = "5.199"

    # Настройки сервера
    server: ServerSettings = Field(default_factory=ServerSettings)

    # Настройки скрэпперов
    scrapper: ScrapperSettings = Field(default_factory=ScrapperSettings)

    # Настройки уведомлений
    notification: NotificationSettings = Field(default_factory=NotificationSettings)

    @property
    def is_local(self) -> bool:

        return self.ENV == "local"

    @property
    def is_test_env(self) -> bool:  # noqa: FNE002
        return self.ENV == "test"

    @field_validator("POSTGRES_DSN", mode="before")
    @classmethod
    def assemble_postgres_dsn(cls, value: str | None, info: ValidationInfo) -> str:
        if isinstance(value, str):
            return value

        dsn = cls._build_postgres_dsn(values=info.data)
        if dsn:
            return str(dsn)

        raise ValueError(value)

    @classmethod
    def _build_postgres_dsn(cls, values: dict[str, Any], db_name: str | None = None) -> PostgresDsn | None:
        if not db_name:
            db_name = values.get("POSTGRES_DB_NAME")

        if (
            db_name
            and values.get("POSTGRES_DB_USER")
            and values.get("POSTGRES_DB_PASSWORD")
            and values.get("POSTGRES_DB_HOST")
            and values.get("POSTGRES_DB_PORT")
        ):
            return PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=values.get("POSTGRES_DB_USER"),
                password=values.get("POSTGRES_DB_PASSWORD"),
                host=values.get("POSTGRES_DB_HOST"),
                port=values.get("POSTGRES_DB_PORT"),
                path=db_name,
            )

        return None


class LoggingSettings(ConfigSettings):
    # main
    DEFAULT_LOG_LEVEL: str = "INFO"
    IS_NEED_LOG_SQL_QUERIES: bool = False

    # uvicorn
    UVICORN_LOG_LEVEL: str = "INFO"
    UVICORN_ACCESS_LOG_LEVEL: str = "INFO"


settings = Settings()
logging_settings = LoggingSettings()
