from pymongo import MongoClient
from config import Config
from app.models.base_model import set_db

def init_db():
    mongo_client = MongoClient(Config.MONGO_URI)
    db = mongo_client[Config.DB_NAME]
    set_db(db)
    return mongo_client, db


