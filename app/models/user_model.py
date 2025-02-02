import bcrypt
from app.models.base_model import BaseModel
from pydantic import BaseModel as PydanticModel, Field

class UserSchema(PydanticModel):
    """Schema for validating user registration data."""
    username: str = Field(..., min_length=3, max_length=20, description="Unique username")
    password: str = Field(..., min_length=6, description="Password (hashed in DB)")
    name: str = Field(..., max_length=50, description="Full name")
    email: str = Field(..., max_length=50, description="Email address")

    class Config:
        from_attributes = True

class UserModel(BaseModel):
    collection_name = "users"

    @classmethod
    def create(cls, username, password, name, email):
        """Hashes password and inserts a new user."""
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user = UserSchema(username=username, password=hashed_password.decode('utf-8'), name=name, email=email)
            return cls.insert_one(user.dict())
        except Exception as e:
            return {"error": str(e)}

    @classmethod
    def get_by_username(cls, username):
        """Fetches a user by username."""
        return cls.find_one({"username": username})

    @classmethod
    def check_password(cls, username, password):
        """Validates user credentials."""
        user = cls.get_by_username(username)
        if not user or not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            return None
        return user
    
    @classmethod
    def get_by_email(cls, email):
        """Fetches a user by email."""
        return cls.find_one({"email": email})
