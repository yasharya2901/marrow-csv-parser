import bcrypt
from app.models.base_model import BaseModel
from pydantic import BaseModel as PydanticModel, Field

class UserSchema(PydanticModel):
    """Schema for validating user registration data."""
    username: str = Field(..., min_length=3, max_length=20, description="Unique username")
    password: str = Field(..., min_length=6, description="Password (hashed in DB)")

    class Config:
        from_attributes = True

class UserModel(BaseModel):
    collection_name = "users"

    @classmethod
    async def create(cls, username, password):
        """Hashes password and inserts a new user."""
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user = UserSchema(username=username, password=hashed_password.decode('utf-8'))
            return await cls.insert_one(user.dict())
        except Exception as e:
            return {"error": str(e)}

    @classmethod
    async def get_by_username(cls, username):
        """Fetches a user by username."""
        return await cls.find_one({"username": username})

    @classmethod
    async def check_password(cls, username, password):
        """Validates user credentials."""
        user = await cls.get_by_username(username)
        if not user or not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            return None
        return user
