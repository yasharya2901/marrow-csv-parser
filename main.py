import os
from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from app.routes.auth_routes import auth_routes
from app.routes.task_routes import task_routes
from app.routes.file_routes import file_routes
from config import Config
from app.utils.error_handler import register_error_handlers

load_dotenv()

app = Flask(__name__)

app.config.from_object(Config)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET")
jwt = JWTManager(app)

app.register_blueprint(auth_routes, url_prefix="/auth")
app.register_blueprint(task_routes, url_prefix="/tasks")
app.register_blueprint(file_routes, url_prefix="/files")

register_error_handlers(app)

@app.route("/")
def home():
    return {"message": "Flask Server is Running!"}

if __name__ == "__main__":
    app.run(port=8000, debug=True)
