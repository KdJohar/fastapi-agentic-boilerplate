---
name: fastapi-vertical-slice
description: Use when adding or changing a FastAPI endpoint in this repository.
---

# FastAPI vertical slice

Map the existing application module and follow this dependency direction:

`routes -> views -> controllers -> helpers -> models/schemas`

## Responsibilities

- Route: path, method, status, dependency injection, and response model.
- View: request/response adaptation only.
- Controller: use-case coordination and transaction boundary.
- Helper: focused, typed database or integration operation.
- Model/schema: persistence and validated public contract.

## Required checks

- Validate all external input with Pydantic.
- Derive authorization and ownership from trusted context.
- Keep errors stable and free of private internals.
- Check idempotency, concurrency, and bounded I/O where relevant.
- Add route contract tests plus a focused controller/helper test for risky logic.
- If persistence changes, invoke `safe-schema-change`.
