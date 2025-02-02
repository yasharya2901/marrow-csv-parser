import uuid
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.file_service import FileService
from app.models.task_model import TaskModel
from app.models.user_model import UserModel
from app.utils.error_handler import APIError, error_response
from app.tasks.process_csv import process_csv_task

file_routes = Blueprint("file_routes", __name__)

@file_routes.route("/upload", methods=["POST"])
@jwt_required()
def upload_file():
    """Allows users to upload CSV files."""
    try:
        user = get_jwt_identity()
        user_data = UserModel.get_by_username(user)
        if not user_data:
            raise APIError("User not found", 404)

        if "file" not in request.files:
            raise APIError("No file provided", 400)

        file = request.files["file"]
        task_id = str(uuid.uuid4())

        file_path = FileService.save_file(file, file.filename)
        if not file_path:
            raise APIError("File could not be saved", 500)

        TaskModel.create(task_id, user, file_path)

        process_csv_task.delay(task_id, file_path)

        return jsonify({
            "task_id": task_id,
            "message": "File uploaded successfully. Please wait while it processes."
        }), 202
    except APIError as e:
        return error_response(e.message, e.status_code)
