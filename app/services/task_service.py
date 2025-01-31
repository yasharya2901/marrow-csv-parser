import pandas as pd
from app.models.task_model import TaskModel
from app.models.movie_model import MovieModel
from app.services.file_service import FileService
import logging

async def process_csv(task_id, file_path):
    """
    Reads a CSV file, inserts data into MongoDB, and deletes the file after processing.
    :param task_id: The associated task ID
    :param file_path: The file path of the uploaded CSV
    """
    try:
        await TaskModel.update_status(task_id, "processing")

        async for chunk in pd.read_csv(file_path, chunksize=5000):
            movies = chunk.to_dict(orient="records")
            await MovieModel.insert_movies(movies)

        await TaskModel.update_status(task_id, "done")

        await FileService.cleanup_file_after_processing(task_id)

    except Exception as e:
        logging.error(f"Error processing CSV for task {task_id}: {e}")
        await TaskModel.update_status(task_id, "failed")
