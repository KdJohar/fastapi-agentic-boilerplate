from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_starter.apps.tasks.controllers import create_task, get_task
from fastapi_starter.apps.tasks.schemas import TaskCreate, TaskRead


async def create_task_view(payload: TaskCreate, session: AsyncSession) -> TaskRead:
    task = await create_task(session, payload)
    return TaskRead.model_validate(task)


async def get_task_view(task_id: UUID, session: AsyncSession) -> TaskRead:
    task = await get_task(session, task_id)
    return TaskRead.model_validate(task)
