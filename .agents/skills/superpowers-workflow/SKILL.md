---
name: superpowers-workflow
description: Use for every non-trivial feature, fix, refactor, or migration. Enforces understand, plan, plan review, test-driven execution, code review, and verification.
---

# Superpowers workflow

This is the repository's focused adaptation of the Superpowers development
methodology. It does not authorize production work or expand the user's scope.

## 1. Understand

- Restate the outcome in observable terms.
- Name constraints, non-goals, affected users/contracts, and approval boundaries.
- Ask only when a missing decision changes behavior, data, security, cost, or
  external state.

## 2. Map

- Use CodeGraph first when `.codegraph/` exists.
- Trace the request path, callers, persistence, contracts, and relevant tests.
- Prefer the `backend_mapper` for bounded read-only evidence.

## 3. Plan and review

- List concrete edits, owned paths, dependencies, risks, and exact checks.
- Use the `plan_reviewer` for material work.
- Resolve critical and high findings before writing code. Record deliberately
  accepted trade-offs.

## 4. Execute with tests

- Write or update the smallest failing behavior test first.
- Make it pass with the smallest complete implementation.
- Keep architecture boundaries and fix every affected caller or fixture.
- Refactor only when the result is simpler or removes duplication already present.

## 5. Review and verify

- Use `contract_guard` for API, data, security, migration, or concurrency risk.
- Use `validation_planner` to select the smallest sufficient targeted checks.
- Inspect the integrated diff, then run `make verify`.
- Report exact results and remaining risk. Evidence, not confidence, closes work.

## Delegation

Delegate independent discovery or review only. Use at most three concurrent
workers, never nested delegation, and keep all edits and integration with the
parent agent.

Based on the MIT-licensed Superpowers project by Jesse Vincent and contributors:
https://github.com/obra/superpowers
