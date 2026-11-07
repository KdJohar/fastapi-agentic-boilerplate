# Project scope

## Purpose

This repository is a reusable FastAPI starter with an AI-assisted development
harness. It demonstrates how to build and verify backend changes with explicit
architecture, scoped agent roles, and production-safe defaults.

## Included decisions

- Organize request handling as routes, views, controllers, helpers, models, and
  schemas.
- Use CodeGraph-first discovery before broad repository reads.
- Keep agent delegation bounded and limited to independent, read-only work.
- Use PostgreSQL, async SQLAlchemy, Alembic, and environment-based configuration.
- Include one complete API example instead of pre-installing unused components.
- Measure runtime reliability and delivery quality before AI activity metrics.
- Keep production actions and final merge decisions under human control.

## Deliberate non-goals

Authentication, queues, caches, tracing backends, cloud deployment, and provider
integrations are not included without a concrete requirement. Their policies and
operational costs depend on the service being built.

## Read next

- `architecture.md` for code boundaries.
- `agentic-development.md` for agents, skills, hooks, and cost controls.
- `developer-velocity.md` for development workflow and measurement.
- `observability.md` for runtime and delivery signals.
