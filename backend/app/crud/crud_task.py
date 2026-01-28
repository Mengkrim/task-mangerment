from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdateFull, TaskUpdatePartial
from typing import List, Optional

async def create_task(db: AsyncSession, task_id: TaskCreate, owner_id: int) -> Task:
    db_task = Task(**task_id.model_dump(), owner_id=owner_id)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def get_task_user(db: AsyncSession, owner_id:int , skip: int = 0, limit: int = 100) -> List[Task]:
    result = await db.execute
    (select(Task).where(Task.owner_id == owner_id).offset(skip).limit(limit).order_by(Task.created_at.desc()))
    return result.scalars().all()

async def update_task(db: AsyncSession, task_id: int, task_Update, owner_id: int) -> Optional[Task]:
    result = await db.execute(select(Task).where(Task.id == task_id, Task.owner_id == owner_id)
    )
    task = result.scalar_one_or_none()
    if not task:
        return None

    update_data = task_Update.model_dump(exclude_unset=True)
    if not update_data:
        return task
    for key, value in update_data.items():
        setattr(task, key, value)

    await db.commit()
    await db.refresh(task)
    return task