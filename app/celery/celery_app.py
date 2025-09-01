from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    imports=["app.workers.outbox_relayer", "app.workers.listen_request_created", "app.workers.listen_request_processed"],
    timezone="UTC",
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    'outbox-relayer': {
        'task': 'run_outbox_relayer',
        'schedule': 5.0,
    },
    'listen-request-created': {
        'task': 'listen_request_created',
        'schedule': 5.0,
    },
    'listen-request-processed': {
        'task': 'listen_request_processed',
        'schedule': 5.0,
    },
}