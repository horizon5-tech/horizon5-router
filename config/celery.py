import os
from logging.config import dictConfig
from typing import Any

from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging
from django.conf import settings

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


@setup_logging.connect
def config_loggers(*args: Any, **kwargs: Any) -> None:  # noqa: ARG001
    dictConfig(settings.LOGGING)


app.autodiscover_tasks()

app.conf.beat_schedule = {
    # "process_backtest_schedule": {
    #     "task": "apps.core.tasks.process_backtest",
    #     "schedule": crontab(minute="*/1"),
    # },
}
