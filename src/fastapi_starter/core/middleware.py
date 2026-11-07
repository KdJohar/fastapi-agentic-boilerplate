from __future__ import annotations

import re
from collections.abc import Awaitable, Callable
from time import perf_counter
from typing import Any
from uuid import uuid4

from prometheus_client import Counter, Histogram
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from fastapi_starter.core.context import reset_request_id, set_request_id

REQUESTS = Counter(
    "http_requests_total",
    "HTTP requests completed by route and status.",
    ("method", "route", "status"),
)
REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration by route.",
    ("method", "route"),
)
_SAFE_REQUEST_ID = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")


class RequestContextMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = _request_id_from_headers(scope) or str(uuid4())
        token = set_request_id(request_id)

        async def send_with_request_id(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                headers.append((b"x-request-id", request_id.encode("ascii")))
                message["headers"] = headers
            await send(message)

        try:
            await self.app(scope, receive, send_with_request_id)
        finally:
            reset_request_id(token)


class MetricsMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or scope.get("path") == "/metrics":
            await self.app(scope, receive, send)
            return

        started = perf_counter()
        status = 500

        async def capture_status(message: Message) -> None:
            nonlocal status
            if message["type"] == "http.response.start":
                status = int(message["status"])
            await send(message)

        try:
            await self.app(scope, receive, capture_status)
        finally:
            route = getattr(scope.get("route"), "path", "unmatched")
            method = str(scope.get("method", "UNKNOWN"))
            REQUESTS.labels(method=method, route=route, status=str(status)).inc()
            REQUEST_DURATION.labels(method=method, route=route).observe(perf_counter() - started)


def _request_id_from_headers(scope: Scope) -> str | None:
    headers: list[tuple[bytes, bytes]] = scope.get("headers", [])
    for name, value in headers:
        if name.lower() == b"x-request-id":
            candidate = value.decode("ascii", errors="ignore")
            return candidate if _SAFE_REQUEST_ID.fullmatch(candidate) else None
    return None


ASGIHandler = Callable[[Scope, Receive, Send], Awaitable[Any]]
