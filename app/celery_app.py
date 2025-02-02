from celery import signals
from app.db import init_db
from app.celery_instance import celery_app
import app.tasks.process_csv


@signals.worker_process_init.connect
def init_celery_mongo(**kwargs):
    """Initialize MongoDB only when a Celery worker starts."""
    mongo_client, db = init_db()  
    celery_app.mongo_client = mongo_client
    celery_app.db = db

