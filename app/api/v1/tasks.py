from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import update, delete
from sqlalchemy.future import select
from app.database.session import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskOut, TaskUpdateFull, TaskUpdatePartial
from typing import List

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# --- Create Task
@router.post("/", response_model=TaskOut, status_code=201)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    db_task = Task(**task.model_dump())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

#--- Get All Tasks
@router.get("/", response_model=list[TaskOut])
async def get_tasks(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Task).offset(skip).limit(limit).order_by(Task.created_at.desc())
    )
    return result.scalars().all()

#--- Get Task by Id
@router.get("/{task_id}", response_model=TaskOut)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# --- Full Update Task
@router.put("/{task_id}", response_model=TaskOut)
async def update_task_full(task_id: int, task_update: TaskUpdateFull, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
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
async def update_task_partial(task_id: int, task_update: TaskUpdatePartial, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    # Partial Update Task
    update_data = task_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    
    stm = (
        update(Task).where(Task.id == task_id).values(**update_data).execution_options(synchronize_session="fetch")
    )

    await db.execute(stm)
    await db.commit()

    # Refresh the get update task
    await db.refresh(task)
    return task

# --- Delete Task
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    await db.delete(task)
    await db.commit()
    return  # ✅ explicit return None

