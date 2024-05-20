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

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "postgres"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432

    MINIO_ACCESS_KEY: str = "minio"
    MINIO_SECRET_KEY: str = "minio123"
    MINIO_HOST: str = "minio"
    MINIO_PORT: int = 9000

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    LOGGING_LEVEL: int = logging.INFO


settings = Settings()
