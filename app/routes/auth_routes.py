from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.services.auth_service import register_user, login_user
from app.utils.error_handler import APIError, error_response

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/register", methods=["POST"])
async def register():
    """Registers a new user."""
    try:
        data = request.json
        if not data or "username" not in data or "password" not in data:
            raise APIError("Username and password are required", 400)

        response, status_code = await register_user(data["username"], data["password"])
        return jsonify(response), status_code
    except APIError as e:
        return error_response(e.message, e.status_code)

@auth_routes.route("/login", methods=["POST"])
async def login():
    """Logs in a user and returns JWT token."""
    try:
        data = request.json
        if not data or "username" not in data or "password" not in data:
            raise APIError("Username and password are required", 400)

        response, status_code = await login_user(data["username"], data["password"])
        return jsonify(response), status_code
    except APIError as e:
        return error_response(e.message, e.status_code)
