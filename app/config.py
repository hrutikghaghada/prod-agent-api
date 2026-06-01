from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # LLM Configuration
    GOOGLE_API_KEY: str | None = None
    PRIMARY_MODEL: str = "gemini-3.1-flash-lite"
    FALLBACK_MODEL: str = "gemini-3.5-flash"

    # LangSmith
    LANGSMITH_API_KEY: str | None = None
    LANGSMITH_TRACING: bool = True
    LANGSMITH_PROJECT: str = "production-api"

    # Application
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    RATE_LIMIT: str = "20/minute"
    CACHE_TTL_SECONDS: int = 300
    MAX_RETRIES: int = 3

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance - loaded once, reused everywhere."""
    return Settings()
