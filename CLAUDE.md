# FastAPI backend — Claude instructions

Read and follow `AGENTS.md`; it is the canonical repository policy. These rules
summarize the behaviors that must remain visible in every Claude Code session.

## Required workflow

For every non-trivial task:

1. Understand the outcome and acceptance criteria.
2. Use CodeGraph first to map affected paths and tests when its index exists.
3. Write a bounded plan with risks and verification commands.
4. Review the plan before editing.
5. Implement the smallest complete change using tests first.
6. Review the integrated diff.
7. Run `make verify` and report evidence before claiming completion.

Use the repository skills in `.agents/skills/`. The `superpowers-workflow` skill
owns the delivery sequence, `ponytail` prevents unnecessary code, and
`codegraph-first` keeps context retrieval focused. Once the requirement and
architecture are accepted, `loadless-engineering-developer` turns them into a
complete vertical slice without inventing new product or architecture decisions.

## Architecture

Keep the dependency direction:

`routes -> views -> controllers -> helpers -> models/schemas`

Routes own HTTP transport, views adapt requests and responses, controllers own
use cases and transactions, helpers own focused I/O, and models/schemas own
persistence and validation. Do not skip layers by querying the database from a
route or returning an HTTP response from a helper.

## Safety

- Never place a credential or production payload in a file, prompt, command,
  commit, log, or PR.
- Never deploy, publish, merge, force-push, run a production migration, or change
  cloud resources without a separate explicit request.
- Challenge unsafe or incorrect assumptions with evidence. Do not agree merely
  to be agreeable.
- Work autonomously within the approved repository and plan. Ask only when a
  missing decision changes behavior, data, security, cost, or external state.

## Commands

- `make run` — start the local API.
- `make test` — run tests with coverage.
- `make lint` — run Ruff checks.
- `make typecheck` — run strict typing.
- `make verify` — run all required checks.

## Commits

Use an imperative conventional subject of at most 50 characters, capitalize its
description, omit the final period, add a blank line, and wrap an explanatory
body at 72 characters. The repository hook enforces these rules.
