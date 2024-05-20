"""
Configuration settings for the application.
"""

import logging

import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    """
    Configuration settings for the application.
    """

    model_config = pydantic_settings.SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_HOST: str
    MINIO_PORT: int

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    LOGGING_LEVEL: int = logging.INFO


settings = Settings()
