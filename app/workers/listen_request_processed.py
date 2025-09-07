from app.celery.celery_app import celery_app
from app.core.redis_client import redis_client
from app.repositories.car_repository import CarRepository
from app.repositories.request_repository import get_request_repository
from app.workers.outbox_relayer import SyncSession

request_repository = get_request_repository()
car_repository = CarRepository()

@celery_app.task(name="workers.listen_request_processed")
def listen_channel():
    with SyncSession() as session:
        with session.begin():
            messages = redis_client.get_messages_from_channel("request_processed", 10)
            print(f"Redis - got {len(messages)} messages")

            for message in messages:
                payload = message.loads(message).get("payload")

                request_record = request_repository.get_by_uuid(payload.get("request_uuid"))

                if request_record:
                    request_repository.mark_as_done(request_record)
                    car_repository.update_or_create(payload.get("vin"), payload)

            session.commit()