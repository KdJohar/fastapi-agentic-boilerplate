import json
import logging

from fastapi_starter.core.context import reset_request_id, set_request_id
from fastapi_starter.core.logging import JsonFormatter


def test_json_formatter_includes_request_context() -> None:
    token = set_request_id("request-123")
    try:
        record = logging.LogRecord(
            name="starter.test",
            level=logging.INFO,
            pathname=__file__,
            lineno=10,
            msg="Task created",
            args=(),
            exc_info=None,
        )
        payload = json.loads(JsonFormatter().format(record))
    finally:
        reset_request_id(token)

    assert payload["message"] == "Task created"
    assert payload["request_id"] == "request-123"
