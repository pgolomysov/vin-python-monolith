import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    redis_url: str
    alembic_database_url: str
    secret_key: str
    debug: bool = False
    event_map: dict = {
        #event:channel
        "request_created": "request_created",
        "request_processed": "request_processed"
    }
    model_config = SettingsConfigDict(
        env_file=".env.test" if os.getenv("PYTEST_CURRENT_TEST") else ".env",
        env_file_encoding="utf-8",
    )

settings = Settings()