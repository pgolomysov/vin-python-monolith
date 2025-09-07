import random
from datetime import datetime, timezone

import redis
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db.db_session import get_async_session
from app.events.request_processed import RequestProcessed
from app.models import OutboxRelayer
from app.models import Request, Car
from app.workers.outbox_relayer import SyncSession

router = APIRouter()

redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)

@router.get("/test")
async def create_request(db: AsyncSession = Depends(get_async_session)):
    channel = "request_created"

    with SyncSession() as session:
        with session.begin():
            messages = redis_client.rpop("request_created", 10) or []
            print(f"Redis - got {len(messages)} messages")
            for message in messages:
                if message:
                    payload = message["payload"]
                    print(payload)

                    car_data = {
                        "vin": message.vin,
                        "is_damaged": random.randint(0, 1),
                        "mileage": random.choice([60000, 70000, 80000, 100000, 150000, 200000]),
                        "owners_count": random.randint(1, 15),
                        "processed_at": str(datetime.now(timezone.utc)),
                    }

                    event = RequestProcessed(car_data)

                    event_model = OutboxRelayer(payload=event.payload(), event_type=event.event_type())
                    session.add(event_model)

            session.commit()


@router.get("/test2")
async def create_request(db: AsyncSession = Depends(get_async_session)):
    channel = "request_created"
    with SyncSession() as session:
        with session.begin():
            messages = redis_client.rpop("request_processed", 10) or []
            print(f"Redis - got {len(messages)} messages")

            #for message in messages:
                # event = json.loads(message)
                # payload = event.get("payload")
            payload = {}
            payload["request_uuid"] = "6daf271a-a95c-47e4-b019-6ecf9c59b58b"
            payload["is_damaged"] = "true"
            print(payload)

            stmt = select(Request).where(Request.uuid == payload.get("request_uuid"))
            result = session.execute(stmt)
            record = result.scalar_one_or_none()
            if record:
                record.done = True

                stmt = select(Car).where(Car.vin == record.vin)
                result = session.execute(stmt)
                car_record = result.scalar_one_or_none()
                print(f" 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥Car record {record.vin}")
                if car_record:
                    car_record.data = payload
                else:
                    car_record = Car()
                    car_record.vin = record.vin
                    car_record.data = payload
                    session.add(car_record)

            session.commit()
