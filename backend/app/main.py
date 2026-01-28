from fastapi import FastAPI

from app.api.v1 import tasks, auth
from app.database.session import engine
from app.database.base import Base
from fastapi.middleware.cors import CORSMiddleware

# IMPORTANT: import models so Base knows them
from app.models import user, task  # noqa: F401


app = FastAPI(
    title="Task Manager API",
    version="1.0.1"
)

origins = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
