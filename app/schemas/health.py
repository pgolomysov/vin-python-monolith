from typing import Literal

from pydantic import BaseModel

class HealthStatus(BaseModel):
    app: Literal["healthy", "unhealthy"]
    redis: Literal["healthy", "unhealthy"]
    database: Literal["healthy", "unhealthy"]
    