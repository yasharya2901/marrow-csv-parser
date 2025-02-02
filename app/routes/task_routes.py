from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.task_model import TaskModel
from app.utils.error_handler import APIError, error_response

task_routes = Blueprint("task_routes", __name__)

@task_routes.route("/task/<task_id>", methods=["GET"])
@jwt_required()
def get_task_status(task_id):
    """Fetches task status for a user."""
    try:
        user = get_jwt_identity()
        task = TaskModel.get_task(task_id)

        if not task:
            raise APIError("Task not found", 404)

        # Ensure users can only view their own tasks
        if task["user"] != user:
            raise APIError("Unauthorized to access this task", 403)

        return jsonify({"task_id": task["task_id"], "status": task["status"]})
    except APIError as e:
        return error_response(e.message, e.status_code)
    
@task_routes.route("/tasks", methods=["GET"])
@jwt_required()
def get_user_tasks():
    """Fetches all tasks for a user."""
    try:
        user = get_jwt_identity()
        tasks = TaskModel.get_task_by_user(user)
        return jsonify(tasks)
    except APIError as e:
        return error_response(e.message, e.status_code)
