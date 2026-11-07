.PHONY: install run test lint format typecheck audit verify migrate hooks agent-setup agent-check

install:
	uv sync --locked --dev

run:
	uv run uvicorn fastapi_starter.main:app --reload --host 0.0.0.0 --port 8000

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff check --fix .
	uv run ruff format .

typecheck:
	uv run mypy

audit:
	uv run pip-audit

verify: lint typecheck test

migrate:
	uv run alembic upgrade head

hooks:
	./scripts/install_hooks.sh

agent-setup:
	./scripts/setup_agent_tools.sh

agent-check:
	./scripts/setup_agent_tools.sh --check --all
