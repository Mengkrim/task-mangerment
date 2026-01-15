from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TaskBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    completed: bool = False

class TaskCreate(TaskBase):
    "Used for task creation - all fields required"
    pass

class TaskUpdateFull(TaskBase):
    "Used for full task update - all fields required"
    pass

class TaskUpdatePartial(BaseModel):
    "Used for partial task update - all fields optional"
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskOut(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # ← important for SQLAlchemy → Pydantic conversion (v2 style)