from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.base import Base

# Optional: Define as string 
TASK_STATUS = ('todo', 'in_progress', "done", "cancelled")
TASK_PRIORITY = ('low', 'medium', 'high')

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    status = Column(String, default="todo", nullable=False)
    priority = Column(String, default="medium")

# New : owner relationship
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="tasks")