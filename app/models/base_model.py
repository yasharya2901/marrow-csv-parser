_db = None

def set_db(db):
    """Sets the database connection for the models."""
    global _db
    _db = db

class BaseModel:
    """A base class for MongoDB models."""
    
    collection_name = None

    @classmethod
    def collection(cls):
        """Returns the MongoDB collection for the model."""
        if _db is None:
            raise Exception("Database not initialized. Call set_db(db) during app startup.")
        return _db[cls.collection_name]

    @classmethod
    def insert_one(cls, document):
        """Insert a single document."""
        return cls.collection().insert_one(document)

    @classmethod
    def insert_many(cls, documents):
        """Insert multiple documents."""
        return cls.collection().insert_many(documents)

    @classmethod
    def find_one(cls, query):
        """Find a single document by query."""
        return cls.collection().find_one(query)

    @classmethod
    def find_all(cls, query={}, limit=100):
        """Find multiple documents with a query."""
        cursor = cls.collection().find(query).limit(limit)
        documents = []
        for document in cursor:
            documents.append(document)
        return documents

    @classmethod
    def update_one(cls, query, update):
        """Update a single document."""
        return cls.collection().update_one(query, {"$set": update})

    @classmethod
    def delete_one(cls, query):
        """Delete a single document."""
        return cls.collection().delete_one(query)
