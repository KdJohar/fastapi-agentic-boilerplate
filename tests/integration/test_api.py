from uuid import UUID

from httpx import AsyncClient


async def test_health_endpoints(client: AsyncClient) -> None:
    live = await client.get("/health/live")
    ready = await client.get("/health/ready")

    assert live.status_code == 200
    assert live.json() == {"status": "ok"}
    assert ready.status_code == 200
    assert ready.json() == {"status": "ok"}


async def test_create_and_read_task(client: AsyncClient) -> None:
    created = await client.post(
        "/api/v1/tasks",
        json={"title": "  Review API plan  "},
        headers={"x-request-id": "starter-test-1"},
    )

    assert created.status_code == 201
    assert created.headers["x-request-id"] == "starter-test-1"
    body = created.json()
    UUID(body["id"])
    assert body["title"] == "Review API plan"
    assert body["is_done"] is False

    fetched = await client.get(f"/api/v1/tasks/{body['id']}")
    assert fetched.status_code == 200
    assert fetched.json() == body


async def test_missing_task_has_stable_error(client: AsyncClient) -> None:
    response = await client.get("/api/v1/tasks/00000000-0000-0000-0000-000000000001")

    assert response.status_code == 404
    body = response.json()
    assert body["detail"] == "Task not found"
    assert body["request_id"] == response.headers["x-request-id"]


async def test_blank_title_is_rejected(client: AsyncClient) -> None:
    response = await client.post("/api/v1/tasks", json={"title": "   "})

    assert response.status_code == 422


async def test_invalid_request_id_is_replaced(client: AsyncClient) -> None:
    response = await client.get(
        "/health/live",
        headers={"x-request-id": "bad request id\nvalue"},
    )

    assert response.status_code == 200
    assert response.headers["x-request-id"] != "bad request id\nvalue"
    UUID(response.headers["x-request-id"])


async def test_metrics_are_exposed(client: AsyncClient) -> None:
    await client.get("/health/live")
    response = await client.get("/metrics")

    assert response.status_code == 200
    assert "http_requests_total" in response.text
    assert 'route="/health/live"' in response.text
