import asyncio
import json

from app.celery.celery_app import celery_app
from app.core.redis.redis_client import RedisSyncClient
from app.repositories.car_repository import get_car_repository_sync
from app.repositories.request_repository import get_request_repository_sync
from app.workers.outbox_relayer import SyncSession
from app.core.logging import logger

redis_client = RedisSyncClient()
@celery_app.task(name="workers.listen_request_processed")
def listen_channel():
    with SyncSession() as db_session:
        with db_session.begin():
            request_repository = get_request_repository_sync(db_session)
            car_repository = get_car_repository_sync(db_session)

            messages = redis_client.get_messages_from_channel("request_processed", 10)
            logger.info(f"🍴 Listen request processed, fetched {len(messages)}")

            for message in messages:
                message = json.loads(message)
                payload = message.get("payload")

                request_record = request_repository.get_by_uuid(payload.get("request_uuid"))

                if request_record:
                    request_repository.mark_as_done(request_record)

                    car_repository.update_or_create(payload.get("vin"), payload)

            db_session.commit()