__all__ = (
    'settings',
)

from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    DATABASE_URL: str

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 180
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60

    APP_PORT: int = 8000
    BOT_TOKEN: str | None = None
    BOT_MODE: Literal["polling", "webhook"] = "polling"
    WEBHOOK_BASE_URL: str | None = None
    WEBHOOK_PATH: str = "/telegram/webhook"
    WEBHOOK_SECRET: str | None = None

    ALLOW_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"


settings = Settings()
