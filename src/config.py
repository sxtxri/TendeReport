import os

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

class Settings(ConfigSettings):
    SERVICE_NAME: str


settings = Settings()