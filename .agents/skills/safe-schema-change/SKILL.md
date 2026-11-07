---
name: safe-schema-change
description: Use for every PostgreSQL model, Alembic migration, backfill, index, constraint, or persistent deletion change.
---

# Safe schema change

This skill never authorizes a production migration.

1. Map every model caller, query, serializer, fixture, and existing revision.
2. Prefer expand/contract compatibility across overlapping application versions.
3. Explain locks, table rewrites, default behavior, index build, backfill bounds,
   and rollback or deliberate non-revertibility.
4. Add one linear Alembic revision and keep downgrade behavior honest.
5. Keep transactions explicit and PostgreSQL authoritative.
6. Test old/new contract compatibility and the changed constraint or query.
7. Run migration checks only against an intentional local or test database.
