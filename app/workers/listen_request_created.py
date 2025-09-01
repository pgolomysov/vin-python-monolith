import json
from datetime import datetime, timezone

from app.celery.celery_app import celery_app
import redis
import random
from app.core.redis_client import RedisClient
from app.events.request_processed import RequestProcessed
from app.services.event.event_system import EventSystem

redis_client = RedisClient()
event_system = EventSystem()

@celery_app.task(name="listen_request_created")
def listen_channel():
    messages = redis_client.get_messages_from_channel("request_created", 10)
    print(f"Redis - got {len(messages)} messages")
    for message in messages:
        payload = json.loads(message).get("payload")

        event_system.dispatch(
            RequestProcessed({
                "vin": payload.get("vin"),
                "request_uuid": payload.get("uuid"),
                "is_damaged": random.randint(0, 1),
                "mileage": random.choice([60000, 70000, 80000, 100000, 150000, 200000]),
                "owners_count": random.randint(1, 15),
                "processed_at": str(datetime.now(timezone.utc)),
            })
        )
