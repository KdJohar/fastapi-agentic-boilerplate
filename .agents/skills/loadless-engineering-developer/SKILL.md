---
name: loadless-engineering-developer
description: Use after a PRD and its architecture decision records are accepted to implement a complete backend change without redesigning the approved contract.
---

# Loadless engineering developer

Turn an approved PRD and accepted architecture decision records into the
smallest production-ready implementation. This skill implements decisions; it
does not create, edit, or supersede them. Stop and ask for a decision when the
inputs conflict or leave a material gap in behavior, data, security, cost, or
rollout. Do not implement a proposed, rejected, deprecated, or superseded
decision without explicit approval.

## Implementation contract

Before editing:

1. Read the complete requirement, accepted decisions, affected code, contracts,
   migrations, tests, and operational guidance.
2. Record the user outcome, non-goals, binding decisions, compatibility needs,
   acceptance checks, and unresolved questions.
3. Map each material requirement to its code, test, and observable evidence.

Do not silently change ownership, source of truth, consistency, authorization,
event meaning, retry behavior, or rollout policy.

## Code boundaries

Preserve the dependency direction:

`routes -> views -> controllers -> helpers -> models/schemas`

- Routes own paths, methods, dependencies, and transport metadata.
- Views adapt validated requests and responses.
- Controllers own use cases and transaction boundaries.
- Helpers own focused database or external I/O.
- Models and schemas own persistence and validated contracts.

Keep external I/O async and bounded. Avoid a database or network round trip per
item. Define bulk limits, partial failure, idempotency, retries, ordering, audit,
and recovery whenever the behavior needs them.

## Definition of done

- Implement one thin, complete vertical slice before expanding the scope.
- Update OpenAPI and contract documentation with every public API change.
- Test acceptance criteria, authorization, failure paths, compatibility,
  concurrency, and performance where they can affect users.
- Add observability only for an actionable SLO or operating decision.
- Keep commits coherent and leave unrelated work untouched.
- Recheck the approved requirement and decisions before handoff.
- Report exact verification evidence, measurements, remaining risk, and any
  decision that still needs a person.
