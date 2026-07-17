from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # Application
    app_name: str = "Profile Automation Tool"
    app_version: str = "0.1.0"
    log_level: str = "INFO"

    # Database
    database_url: str = "sqlite:///./storage/profile_automation.db"

    # Profile Validation
    pass_score_max: int = 30
    result_timeout_seconds: int = 60

    # Controller
    controller_host: str = "127.0.0.1"
    controller_port: int = 8080

    # Browser
    headless: bool = False

    # Job Settings
    target_profiles: int = 10
    max_concurrent: int = 5

    # Verisoul
    collect_ms: int = 10000
    pending_drain_ms: int = 3000

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()