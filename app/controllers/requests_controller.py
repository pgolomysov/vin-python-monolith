import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.events.request_created import RequestCreated
from app.models import Request, Car
from app.repositories.request_repository import RequestRepository
from app.schemas.requests.request_create import RequestCreate
from app.services.event.event_system import EventSystem

router = APIRouter()

@router.post("/requests")
async def create_request(
        request: RequestCreate,
        db: AsyncSession = Depends(get_session),
        event_system: EventSystem = Depends(EventSystem),
        request_repository: RequestRepository = Depends(RequestRepository),
):
    request_model = request_repository.create(uuid=uuid.uuid4(), email=request.email, vin=request.vin)
    await db.flush()
    await db.commit()

    event = RequestCreated({
        "uuid": str(request_model.uuid),
        "vin": request_model.vin,
        "email": request_model.email,
        "created_at": str(request_model.created_at),
    })

    await event_system.dispatch(event)

    return {
        "request": {
            "vin": request_model.vin,
            "email": request_model.email,
        }
    }

@router.get("/requests")
async def get_requests(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Request))
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
async def get_requests(uuid: str, session: AsyncSession = Depends(get_session)):
    try:
        stmt = select(Request).where(Request.uuid == uuid)
        result = await session.execute(stmt)
        request = result.scalars().one_or_none()
    except Exception:
        raise HTTPException(status_code=404, detail="Request not found")

    if request and request.done is True:
        stmt = select(Car).where(Car.vin == request.vin)
        result = await session.execute(stmt)
        car = result.scalars().one_or_none()

        return car.data
    else:
        return {
            "done": False
        }
