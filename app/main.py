from fastapi import FastAPI

from app.api.v1 import tasks, auth
from app.database.session import engine
from app.database.base import Base

# IMPORTANT: import models so Base knows them
from app.models import user, task  # noqa: F401


app = FastAPI(
    title="Task Manager API",
    version="1.0.1"
)


@app.on_event("startup")
async def startup_event():
    """Create database tables on application startup (async-safe)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(tasks.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Welcome to Task Manager API"}
