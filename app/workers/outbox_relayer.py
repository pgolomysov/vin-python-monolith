import json
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.celery.celery_app import celery_app
from app.core.config import settings
from app.core.redis_client import RedisSyncClient
from app.repositories.outbox_relayer_repository import get_outbox_relayer_repository

sync_engine = create_engine(settings.alembic_database_url, echo=True, future=True)
SyncSession = sessionmaker(bind=sync_engine, expire_on_commit=False)
redis_client = RedisSyncClient()

@celery_app.task(name="workers.run_outbox_relayer")
def run_outbox_relayer():
    with SyncSession() as db_session:
        with db_session.begin():
            outbox_relayer_repository = get_outbox_relayer_repository(db_session)

            sys.stdout.flush()
            events = outbox_relayer_repository.get(10)

            for e in events:
                payload = json.dumps({
                    "id": e.id,
                    "event_type": e.event_type,
                    "payload": e.payload,
                })

                channel = settings.event_map.get(e.event_type)

                if channel is None:
                    #TODO: add DLQ
                    raise Exception("No channel for event found")

                print(f"Pushed to channel {channel}: {payload}")
                redis_client.push_event_to_channel(channel, payload)

                outbox_relayer_repository.mark_consumed(e)

        db_session.commit()
        print("Finishing outbox relayer")

        return {"processed": len(events)}
