from app.celery_app import celery_app
import asyncio
import logging
from app.services.task_service import process_csv

@celery_app.task(name="process_csv_task")
def process_csv_task(task_id, file_path):
    try:
        process_csv(task_id, file_path)
    except Exception as e:
        logging.error(f"Error in process_csv_task for task_id {task_id}: {e}")
