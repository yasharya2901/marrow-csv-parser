import motor.motor_asyncio
from config import Config

client = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGO_URI)
db = client[Config.DB_NAME]

class BaseModel:
    """A base class for MongoDB models."""
    
    collection_name = None

    @classmethod
    def collection(cls):
        """Returns the MongoDB collection for the model."""
        return db[cls.collection_name]

    @classmethod
    async def insert_one(cls, document):
        """Insert a single document."""
        return await cls.collection().insert_one(document)

    @classmethod
    async def insert_many(cls, documents):
        """Insert multiple documents."""
        return await cls.collection().insert_many(documents)

    @classmethod
    async def find_one(cls, query):
        """Find a single document by query."""
        return await cls.collection().find_one(query)

    @classmethod
    async def find_all(cls, query={}, limit=100):
        """Find multiple documents with a query."""
        cursor = cls.collection().find(query).limit(limit)
        documents = []
        async for document in cursor:
            documents.append(document)
        return documents

    @classmethod
    async def update_one(cls, query, update):
        """Update a single document."""
        return await cls.collection().update_one(query, {"$set": update})

    @classmethod
    async def delete_one(cls, query):
        """Delete a single document."""
        return await cls.collection().delete_one(query)
