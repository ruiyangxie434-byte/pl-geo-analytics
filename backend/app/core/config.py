from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PL Geo Analytics API"
    app_env: str = "development"
    app_version: str = "0.1.0"
    debug: bool = True
    api_prefix: str = "/api"
    frontend_origins: str = "http://localhost:3000"
    database_url: str = "sqlite:///./pl_geo_analytics.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.frontend_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
