import pandas as pd
import logging
from app.models.task_model import TaskModel
from app.models.movie_model import MovieModel
from app.services.file_service import FileService

def process_csv(task_id, file_path):
    try:
        TaskModel.update_status(task_id, "processing")
        for chunk in pd.read_csv(file_path, chunksize=5000):
            movies = chunk.to_dict(orient="records")
            MovieModel.insert_movies(movies)
        TaskModel.update_status(task_id, "done")
        FileService.cleanup_file_after_processing(task_id)
    except Exception as e:
        TaskModel.update_status(task_id, "failed")
        logging.error(f"Error processing CSV for task {task_id}: {e}")
