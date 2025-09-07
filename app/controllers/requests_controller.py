import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.db_session import get_async_session
from app.events.request_created import RequestCreated
from app.models import Request, Car
from app.repositories.request_repository import RequestRepositoryAsync, get_request_repository_async
from app.schemas.requests.request_create import RequestCreate
from app.services.event.event_service import EventServiceAsync, get_async_event_service

router = APIRouter()

@router.post("/requests")
async def create_request(
        request: RequestCreate,
        db: AsyncSession = Depends(get_async_session),
        event_service: EventServiceAsync = Depends(get_async_event_service),
        request_repository: RequestRepositoryAsync = Depends(get_request_repository_async),
):
    request_model = await request_repository.create(uuid=uuid.uuid4(), email=request.email, vin=request.vin)
    await db.flush()
    await db.commit()

    event = RequestCreated({
        "uuid": str(request_model.uuid),
        "vin": request_model.vin,
        "email": request_model.email,
        "created_at": str(request_model.created_at),
    })

    await event_service.dispatch(event)

    return {
        "request": {
            "vin": request_model.vin,
            "email": request_model.email,
            "request_id": str(request_model.uuid),
        }
    }

@router.get("/requests")
async def get_requests(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Request))
    requests = result.scalars().all()

    return {
        "requests": [
            {
                "uuid": request.uuid,
                "vin": request.vin,
                "email": request.email,
                "done": request.done,
                "created_at": request.created_at,
                "updated_at": request.updated_at
            } for request in requests
        ]
    }

@router.get("/requests/{uuid}")
async def get_requests(uuid: str, db: AsyncSession = Depends(get_async_session)):
    try:
        stmt = select(Request).where(Request.uuid == uuid)
        result = await db.execute(stmt)
        request = result.scalars().one_or_none()
    except Exception:
        raise HTTPException(status_code=404, detail="Request not found")

    # If request is done, we return latest car data
    if request and request.done is True:
        stmt = select(Car).where(Car.vin == request.vin)
        result = await db.execute(stmt)
        car = result.scalars().one_or_none()

        return car.data
    else:
        return {
            "done": False
        }
