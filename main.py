from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from app.db import init_db
from app.routes.auth_routes import auth_routes
from app.routes.task_routes import task_routes
from app.routes.file_routes import file_routes
from app.routes.movie_routes import movie_routes
from config import Config
from app.utils.error_handler import register_error_handlers
from asgiref.wsgi import WsgiToAsgi
import uvicorn
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    JWTManager(app)

    app.register_blueprint(auth_routes, url_prefix="/auth")
    app.register_blueprint(task_routes, url_prefix="/tasks")
    app.register_blueprint(file_routes, url_prefix="/files")
    app.register_blueprint(movie_routes, url_prefix="/movies")
    
    register_error_handlers(app)
    
    @app.route("/")
    def home():
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
        return send_from_directory(static_dir, "index.html")
    
    
    return app

app = create_app()
mongo_client, db = init_db()
app.mongo_client = mongo_client
app.db = db

asgi_app = WsgiToAsgi(app)

if __name__ == "__main__":
    uvicorn.run(asgi_app, host=Config.HOST, port=Config.PORT, log_level="debug")