import uuid
import asyncio
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.task_service import process_csv
from app.services.file_service import FileService
from app.models.task_model import TaskModel
from app.models.user_model import UserModel
from app.utils.error_handler import APIError, error_response

file_routes = Blueprint("file_routes", __name__)

@file_routes.route("/upload", methods=["POST"])
@jwt_required()
async def upload_file():
    """Allows users to upload CSV files."""
    try:
        user = get_jwt_identity()
        user_data = await UserModel.get_by_username(user)
        if not user_data:
            raise APIError("User not found", 404)

        if "file" not in request.files:
            raise APIError("No file provided", 400)

        file = request.files["file"]
        task_id = str(uuid.uuid4())

        file_path = await FileService.save_file(file, file.filename)
        if not file_path:
            raise APIError("File could not be saved", 500)

        await TaskModel.create(task_id, user, file_path)

        asyncio.create_task(process_csv(task_id, file_path))

        return jsonify({"task_id": task_id, "message": "File uploaded successfully. Please wait till it processes."}), 202
    except APIError as e:
        return error_response(e.message, e.status_code)
