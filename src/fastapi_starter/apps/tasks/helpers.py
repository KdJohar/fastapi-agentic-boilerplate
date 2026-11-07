from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_starter.apps.tasks.models import Task


async def insert_task(session: AsyncSession, *, title: str) -> Task:
    task = Task(title=title)
    session.add(task)
    await session.flush()
    return task


async def fetch_task(session: AsyncSession, *, task_id: UUID) -> Task | None:
    result = await session.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()
