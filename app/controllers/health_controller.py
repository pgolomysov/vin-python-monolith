from fastapi import APIRouter, Depends
from app.core.redis.redis_client import redis_client
from app.schemas.health import HealthStatus
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Request
from app.core.db.db_session import get_async_session

router = APIRouter()

@router.get("/health", response_model=HealthStatus)
async def get_health(session: AsyncSession = Depends(get_async_session)) -> HealthStatus:
    try:
        result = await session.execute(select(Request).limit(1))
        result.scalar_one_or_none()
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"

    try:
        pong = await redis_client.ping()
        redis_status = "healthy" if pong else "unhealthy"
    except Exception:
        redis_status = "unhealthy"

    return HealthStatus(
        app="healthy",
        redis=redis_status,
        database=db_status,
    )