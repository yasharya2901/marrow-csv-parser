import os
import aiofiles
from app.models.task_model import TaskModel
import logging

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class FileService:
    """Handles file operations like saving and deleting uploaded CSV files."""

    @staticmethod
    async def save_file(file, filename):
        """
        Saves an uploaded file asynchronously.
        :param file: File object
        :param filename: Name of the file to be saved
        :return: File path
        """
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        try:
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(file.read())
            return file_path
        except Exception as e:
            logging.error(f"Error saving file: {e}")
            return None

    @staticmethod
    async def delete_file(file_path):
        """
        Deletes a file from the server after processing is completed.
        :param file_path: Path to the file
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logging.info(f"File {file_path} deleted successfully.")
            else:
                logging.warning(f"File {file_path} not found for deletion.")
        except Exception as e:
            logging.error(f"Error deleting file {file_path}: {e}")

    @staticmethod
    async def cleanup_file_after_processing(task_id):
        """
        Deletes the file associated with a task once processing is completed.
        :param task_id: The task ID associated with the file
        """
        task = await TaskModel.get_task(task_id)
        if task and task["status"] == "done":
            await FileService.delete_file(task["file_path"])
