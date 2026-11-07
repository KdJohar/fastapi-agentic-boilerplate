from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_starter.apps.tasks.helpers import fetch_task, insert_task
from fastapi_starter.apps.tasks.models import Task
from fastapi_starter.apps.tasks.schemas import TaskCreate
from fastapi_starter.core.errors import NotFoundError


async def create_task(session: AsyncSession, payload: TaskCreate) -> Task:
    try:
        task = await insert_task(session, title=payload.title)
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    return task


async def get_task(session: AsyncSession, task_id: UUID) -> Task:
    task = await fetch_task(session, task_id=task_id)
    if task is None:
        raise NotFoundError("Task not found")
    return task
