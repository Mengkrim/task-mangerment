# Make Base and all models easily importable from app.models.*
from .base import Base

# Optional: re-export models for convenience
from .user import User
from .task import Task