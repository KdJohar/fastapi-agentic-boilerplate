from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_starter.apps.tasks.schemas import TaskCreate, TaskRead
from fastapi_starter.apps.tasks.views import create_task_view, get_task_view
from fastapi_starter.db.session import get_session

router = APIRouter(prefix="/tasks", tags=["tasks"])
SessionDependency = Annotated[AsyncSession, Depends(get_session)]


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreate, session: SessionDependency) -> TaskRead:
    return await create_task_view(payload, session)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(task_id: UUID, session: SessionDependency) -> TaskRead:
    return await get_task_view(task_id, session)
