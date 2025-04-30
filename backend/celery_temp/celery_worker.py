from celery import Celery
import logging

logging.basicConfig(level=logging.INFO)

celery_app = Celery(
    "worker", broker="redis://redis:6379/0", backend="redis://redis:6379/0"
)

import celery_temp.tasks

celery_app.autodiscover_tasks(["celery_temp"])

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    worker_send_task_events=True,  # Enable task events for monitoring
    task_send_sent_event=True,
)

if __name__ == "__main__":
    celery_app.start()
