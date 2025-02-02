from celery import Celery, signals
from config import Config
from app.db import init_db

celery_app = Celery(
    'tasks',
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND
)

celery_app.conf.update({
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json'],
    'timezone': 'UTC',
    'enable_utc': True,
})

@signals.worker_process_init.connect
def init_celery_mongo(**kwargs):
    """Initialize MongoDB only when a Celery worker starts."""
    mongo_client, db = init_db()  
    celery_app.mongo_client = mongo_client
    celery_app.db = db

