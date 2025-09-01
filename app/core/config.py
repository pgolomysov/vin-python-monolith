from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    alembic_database_url: str
    secret_key: str
    debug: bool = False
    event_map: dict = {
        #event:channel
        "public.request_created": "request_created",
        "public.request_processed": "request_processed"
    }

    class Config:
        env_file = ".env"

settings = Settings()