import bcrypt
from flask_jwt_extended import create_access_token
from app.models.user_model import UserModel
from config import Config
import datetime

def register_user(username, password, name, email):
    """Handles user registration with password hashing."""

    existing_user = UserModel.get_by_username(username)
    if existing_user:
        return {"error": "User with the username already exists"}, 400
    
    existing_user = UserModel.get_by_email(email)
    if existing_user:
        return {"error": "User with the email already exists"}, 400

    UserModel.create(username=username, password=password, name=name, email=email)
    
    access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(minutes=Config.JWT_ACCESS_TOKEN_EXPIRY_MINUTES))
    return {"message": "User registered successfully", "access_token":access_token}, 201

def login_user(username, password):
    """Handles user authentication and JWT creation."""
    user = UserModel.get_by_username(username)
    if not user:
        return {"error": "User not found"}, 404
    
    if not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
        return {"error": "Invalid credentials"}, 401

    access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(minutes=Config.JWT_ACCESS_TOKEN_EXPIRY_MINUTES))

    return {"message":"User logged in successfully", "access_token": access_token}, 200
