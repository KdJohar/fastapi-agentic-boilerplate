import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from fastapi_starter import __version__
from fastapi_starter.api.router import api_router
from fastapi_starter.core.config import Settings, get_settings
from fastapi_starter.core.context import get_request_id
from fastapi_starter.core.errors import NotFoundError
from fastapi_starter.core.logging import configure_logging
from fastapi_starter.core.middleware import MetricsMiddleware, RequestContextMiddleware

logger = logging.getLogger(__name__)


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved = settings or get_settings()
    configure_logging(resolved.log_level)

    app = FastAPI(
        title=resolved.name,
        version=__version__,
        docs_url="/docs" if resolved.expose_docs else None,
        redoc_url=None,
        openapi_url="/openapi.json" if resolved.expose_docs else None,
    )
    app.add_middleware(MetricsMiddleware)
    app.add_middleware(RequestContextMiddleware)
    app.include_router(api_router)

    @app.get("/metrics", include_in_schema=False)
    async def metrics() -> Response:
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    @app.exception_handler(NotFoundError)
    async def not_found_handler(_request: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.detail, "request_id": get_request_id()},
        )

    @app.exception_handler(Exception)
    async def unexpected_error_handler(_request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled request error", exc_info=exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error", "request_id": get_request_id()},
        )

    return app


app = create_app()
