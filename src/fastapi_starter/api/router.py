from fastapi import APIRouter

from fastapi_starter.api.routes.health import router as health_router
from fastapi_starter.apps.tasks.routes import router as tasks_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(tasks_router, prefix="/api/v1")
