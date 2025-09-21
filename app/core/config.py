import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

env = os.getenv("ENV", "prod")

# TODO: beautify
BASE_DIR = Path(__file__).resolve().parent.parent.parent


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
        env_file= BASE_DIR / ".env.test" if env == "test" else ".env",
        env_file_encoding="utf-8",
    )

settings = Settings()