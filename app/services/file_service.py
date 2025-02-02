import os
from app.models.task_model import TaskModel
import logging
from config import Config

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class FileService:
    """Handles file operations like saving and deleting uploaded CSV files."""

    @staticmethod
    def save_file(file, filename):
        """
        Saves an uploaded file to server.
        :param file: File object
        :param filename: Name of the file to be saved
        :return: File path
        """
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        try:
            with open(file_path, "wb") as f:
                f.write(file.read())
            return file_path
        except Exception as e:
            logging.error(f"Error saving file: {e}")
            return None

    @staticmethod
    def delete_file(file_path):
        """
        Deletes a file from the server after processing is completed.
        :param file_path: Path to the file
        """
        try:
            upload_dir = Config.UPLOAD_DIR
            file_path = os.path.join(upload_dir, file_path.split("/")[-1])
            if os.path.exists(file_path):
                os.remove(file_path)
                logging.info(f"File {file_path} deleted successfully.")
            else:
                logging.warning(f"File {file_path} not found for deletion.")
        except Exception as e:
            logging.error(f"Error deleting file {file_path}: {e}")

    @staticmethod
    def cleanup_file_after_processing(task_id):
        """
        Deletes the file associated with a task once processing is completed.
        :param task_id: The task ID associated with the file
        """
        task = TaskModel.get_task(task_id)
        if task and task["status"] == "done":
            FileService.delete_file(task["file_path"])
