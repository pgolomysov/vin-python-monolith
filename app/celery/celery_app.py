from celery import Celery

from app.core.config import settings
from app import workers

celery_app = Celery("worker")

celery_app.conf.update(
    broker_url=settings.redis_url,
    result_backend=settings.redis_url,
    timezone="UTC",
    enable_utc=True,
)

celery_app.conf.update(
    imports=["app.workers.outbox_relayer", "app.workers.listen_request_created", "app.workers.listen_request_processed"],
)

celery_app.conf.beat_schedule = {
    'outbox-relayer': {
        'task': 'workers.run_outbox_relayer',
        'schedule': 5.0,
    },
    'listen-request-created': {
        'task': 'workers.listen_request_created',
        'schedule': 5.0,
    },
    'listen-request-processed': {
        'task': 'workers.listen_request_processed',
        'schedule': 5.0,
    },
}