import bcrypt
from flask_jwt_extended import create_access_token
from app.models.user_model import UserModel

async def register_user(username, password):
    """Handles user registration with password hashing."""

    existing_user = await UserModel.get_by_username(username)
    if existing_user:
        return {"error": "User already exists"}, 400

    await UserModel.create(username=username, password=password)
    
    access_token = create_access_token(identity=username)
    return {"message": "User registered successfully", "access_token":access_token}, 201

async def login_user(username, password):
    """Handles user authentication and JWT creation."""
    user = await UserModel.get_by_username(username)
    if not user:
        return {"error": "User not found"}, 404
    
    if not bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        return {"error": "Invalid credentials"}, 401

    access_token = create_access_token(identity=username)
    return {"message":"User logged in successfully", "access_token": access_token}
