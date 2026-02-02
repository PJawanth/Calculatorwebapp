"""Application configuration with safe defaults."""

import os
from functools import lru_cache


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self) -> None:
        self.app_name: str = os.getenv("APP_NAME", "Calculator WebApp")
        self.env: str = os.getenv("ENV", "development")
        self.debug: bool = os.getenv("DEBUG", "false").lower() == "true"
        self.host: str = os.getenv("HOST", "0.0.0.0")  # noqa: S104
        self.port: int = int(os.getenv("PORT", "8000"))


@lru_cache
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()
