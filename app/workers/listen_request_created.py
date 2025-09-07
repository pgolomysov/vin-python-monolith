import json
import random
from datetime import datetime, timezone

from app.celery.celery_app import celery_app
from app.core.logging import logger
from app.core.redis.redis_client import RedisSyncClient
from app.events.request_processed import RequestProcessed
from app.services.event.event_service import EventServiceSync
from app.workers.outbox_relayer import SyncSession

redis_client = RedisSyncClient()

@celery_app.task(name="workers.listen_request_created")
def listen_channel():
    with SyncSession() as db_session:
        event_service = EventServiceSync(db_session)

        messages = redis_client.get_messages_from_channel("request_created", 10)
        logger.info(f"🍴 Listen request created, fetched {len(messages)}")
        for message in messages:
            payload = json.loads(message).get("payload")

            event_service.dispatch(
                RequestProcessed({
                    "vin": payload.get("vin"),
                    "request_uuid": payload.get("uuid"),
                    "is_damaged": random.randint(0, 1),
                    "mileage": random.choice([60000, 70000, 80000, 100000, 150000, 200000]),
                    "owners_count": random.randint(1, 15),
                    "processed_at": str(datetime.now(timezone.utc)),
                })
            )
