from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import update, delete
from sqlalchemy.future import select
from app.database.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.crud.crud_task import create_task, get_task_user, update_task
from app.schemas.task import TaskCreate, TaskOut, TaskUpdateFull, TaskUpdatePartial
from typing import List

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# --- Create Task
@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_new_task(task_in: TaskCreate, db: AsyncSession = Depends(get_db)):
    # current_user: User = Depends(get_current_user)
    # Replace current_user.id with a placeholder or handle user logic appropriately
    task = await create_task(db, task_in, user_id=None)
    return task

#--- Get All Tasks
@router.get("/", response_model=list[TaskOut])
async def read_my_tasks(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    tasks= await get_task_user(db, current_user_id=current_user.id, skip=skip, limit=limit)
    return tasks

#--- Get Task by Id
@router.get("/{task_id}", response_model=TaskOut)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(task).where(task.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# --- Full Update Task
@router.put("/{task_id}", response_model=TaskOut)
async def update_task_full(task_id: int, task_update: TaskUpdateFull, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(task).where(task.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    # Full Update Task
    for key, value in task_update.model_dump().items():
        setattr(task, key, value)
    
    # db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

# ---- Partail Update Task
@router.patch("/{task_id}", response_model=TaskOut)
async def update_my_task(
    task_id: int,
    task_update: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = await update_task(db, task_id, task_update, current_user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found or not yours")
    return updated

# --- Delete Task
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(task).where(task.id == task_id))
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    await db.delete(task)
    await db.commit()
    return  # ✅ explicit return None

