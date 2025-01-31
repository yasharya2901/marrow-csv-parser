from app.models.base_model import BaseModel
from pydantic import BaseModel as PydanticModel, Field
from typing import Literal

class TaskSchema(PydanticModel):
    """Schema for validating task data before insertion."""
    task_id: str = Field(..., description="Unique Task ID")
    user: str = Field(..., description="User who uploaded the file")
    status: Literal["pending", "processing", "done"] = Field("pending", description="Task status")
    file_path: str = Field(..., description="Path of the uploaded CSV file")

    class Config:
        from_attributes = True

class TaskModel(BaseModel):
    collection_name = "tasks"

    @classmethod
    async def create(cls, task_id, user, file_path):
        """Validates and inserts a task entry."""
        try:
            task = TaskSchema(task_id=task_id, user=user, status="pending", file_path=file_path)
            return await cls.insert_one(task.dict())
        except Exception as e:
            return {"error": str(e)}

    @classmethod
    async def update_status(cls, task_id, status):
        """Updates task status with validation."""
        if status not in ["pending", "processing", "done"]:
            return {"error": "Invalid status"}
        return await cls.update_one({"task_id": task_id}, {"status": status})

    @classmethod
    async def get_task(cls, task_id):
        """Fetches a task by task ID."""
        return await cls.find_one({"task_id": task_id})
