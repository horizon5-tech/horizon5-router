import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

app = Celery("horizon5_router")

app.conf.update(
    broker_url=os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/1"),
    result_backend=os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/1"),
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone=os.environ.get("TZ", "UTC"),
    enable_utc=True,
    broker_connection_retry_on_startup=True,
)

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "process_backtests_schedule": {
        "task": "apps.core.tasks.process_backtests",
        "schedule": crontab(minute="*/1"),
    },
}
