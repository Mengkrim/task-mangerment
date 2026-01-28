from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal

# Use Literral for better edition support & Validation
StatusType = Literal['todo', 'in_progress', 'done', 'cancelled']
PriorityType = Literal['low', 'medium', 'high']


class TaskBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    completed: bool = False
    status: StatusType = "todo"
    priority: PriorityType = "medium"

class TaskCreate(TaskBase):
    "Used for task creation - all fields required"
    pass

class TaskUpdateFull(TaskBase):
    "Used for full task update - all fields required"
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusType] = None
    priority: Optional[PriorityType] = None
    completed: Optional[bool] = None
    
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