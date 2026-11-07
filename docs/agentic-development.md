# Agentic development harness

## Purpose

AI multiplies velocity here by compressing repeatable work—mapping, scaffolding,
test selection, contract review, and documentation—while engineers retain the
decisions that carry product, architecture, security, or production risk.

## Tool setup

Run the repository setup script and choose Claude Code, Codex, or both:

```bash
./scripts/setup_agent_tools.sh
```

It checks the bundled skills, Node.js, both client CLIs, Superpowers, Ponytail,
CodeGraph client configuration, and the local CodeGraph index. Missing components
produce warnings. Installation requires confirmation unless `--yes` is supplied.
Use `--check --all` for a read-only audit.

## Workflow

| Stage | Default tool or role | Output |
|---|---|---|
| Understand | Parent agent | Acceptance criteria and boundaries |
| Map | CodeGraph + `backend_mapper` | Execution path and blast radius |
| Plan | Superpowers workflow | Paths, risks, checks, non-goals |
| Review plan | `plan_reviewer` | Corrected plan or explicit trade-offs |
| Execute | Parent + Loadless Developer + FastAPI skill + Ponytail | Traceable tested change |
| Review contracts | `contract_guard` | Evidence-based findings |
| Verify | `validation_planner` + `make verify` | Reproducible evidence |

The parent is the only writer. Read-only roles can run concurrently only when
their questions are independent; three threads is a ceiling.

`loadless-engineering-developer` begins after the requirement and architecture
are accepted. It preserves those decisions through implementation, API
documentation, failure handling, tests, observability, and handoff. A material
decision gap goes back to a person instead of being filled with an assumption.

## Cost controls

- CodeGraph retrieves relevant symbols instead of repeatedly loading the repo.
- Low-cost roles map paths and choose tests; stronger reasoning reviews plans and
  high-risk contracts.
- Targeted tests run during iteration. Full verification runs at integration
  milestones, not after every line edit.
- Concise subagent output is capped at ten bullets and never includes source dumps.
- Token or cost telemetry must be aggregate and must never store prompts, code,
  payloads, credentials, or personal data.

## Guardrails

The pre-tool policy blocks credential-like commands, forceful Git operations,
publishing, production markers, cluster/cloud mutation, database downgrade, and
broad recursive deletion. Claude Code also denies reads of `.env` files. These
hooks are local safety rails; permissions, branch protection, code review, and
human approval remain authoritative.

The commit hook enforces subject length, capitalization, punctuation, imperative
mood, blank-line separation, body presence, and 72-character body wrapping.

## Superpowers

The repository includes a focused `superpowers-workflow` skill so the core loop
works without a global plugin. For the full upstream library, install the official
MIT-licensed Superpowers plugin with the setup script or your client:

- Codex: open `/plugins`, search for `Superpowers`, and install it.
- Claude Code: `/plugin install superpowers@claude-plugins-official`.

Upstream: https://github.com/obra/superpowers

The local policy wins when a generic upstream workflow conflicts with repository
safety, architecture, scope, or human authorization.

## CodeGraph

CodeGraph is local discovery infrastructure, not a committed database. Run
`codegraph init` once and `codegraph sync` only when source changes make the index
stale enough to affect the task. The local `codegraph-first` skill explains how to
ask for one bounded execution path and its tests.

## Ponytail

Ponytail constrains the solution after the workflow identifies the need. It asks
whether the feature must exist, whether the repository already solves it, and
whether standard-library or installed functionality is sufficient. It never cuts
validation, security, error handling, tests for risky behavior, or requested scope.

The repository bundles a focused Ponytail skill. The setup script can also install
the full upstream plugin for Claude Code and Codex.
