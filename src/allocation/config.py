import logging

import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    POSTGRES_URI: str = "sqlite:///:memory:"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    LOGGING_LEVEL: int = logging.INFO


settings = Settings()
