from pydantic import BaseModel

class HealthStatus(BaseModel):
    app: str
    redis: str
    database: str