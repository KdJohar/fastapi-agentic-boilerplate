# AI-assisted development and measurement

## Where AI saves time

Use AI for frequent work with clear verification:

1. Map an unfamiliar request path and its tests before editing.
2. Turn a request into a reviewed implementation plan with explicit non-goals.
3. Scaffold a complete FastAPI vertical slice instead of disconnected route code.
4. Generate the first regression or contract test and iterate red-green-refactor.
5. Review API, data, authorization, concurrency, and migration compatibility.
6. Select the smallest sufficient tests and produce a concise change summary.

Developers continue to own product intent, architecture trade-offs, sensitive
data, production actions, and merge decisions.

## Example workflow

For a request such as “add task completion”:

1. `backend_mapper` uses CodeGraph to trace the existing create/read flow.
2. The primary agent proposes schema, controller, helper, migration, and test
   changes.
3. `plan_reviewer` challenges concurrency, idempotency, and compatibility gaps.
4. The primary agent writes a failing contract test and the smallest code change.
5. `contract_guard` checks the integrated diff and transaction boundary.
6. `validation_planner` selects targeted tests; `make verify` closes the change.
7. A compliant commit and human-reviewed pull request carry the verified result.

This is faster because AI reduces search, boilerplate, and review latency while
engineering controls remain in place.

## Instrument first

Capture a two-to-four-week baseline before claiming improvement.

| Priority | Measure | Why first |
|---|---|---|
| 1 | PR cycle time split into work and wait | Shows where delivery stalls |
| 2 | Review pickup and revision rounds | Reveals queueing and unclear plans |
| 3 | First-pass CI success and flaky-test rate | Separates speed from rework |
| 4 | Deployment frequency and lead time | Connects merged work to shipped value |
| 5 | Change failure and recovery time | Prevents speed from hiding instability |
| 6 | Escaped defects and rollback rate | Measures user-facing quality |

Then add AI-specific measures:

- Plan approval or material-revision rate
- Contract-review true positives and false positives
- Verification failures caught before human review
- Rework after AI-authored changes
- Cost and elapsed time per accepted change

Do not use lines of code, prompt count, or individual commit count as productivity
metrics. Compare similar work types and use trends, not rankings.

## Runtime instrumentation

The starter includes request rate, route-template latency, status and error rate,
request IDs, structured logs, database readiness, version, and environment. Add
the next metric only when it supports an SLO or an operating decision.

## First-month adoption plan

Start with one important workflow and expand only when the evidence supports it.

| Week | Work | Deliverable | Decision signal |
|---|---|---|---|
| 1 | Map the critical path and capture delivery and runtime baselines | Code-path map, risk register, baseline dashboard, fixed evaluation set | Known bottlenecks and agreed definitions |
| 2 | Pilot reviewed plans, regression tests, and contract review on a small change | One verified vertical slice and recorded human review findings | Plan revision rate, review pickup, first-pass CI |
| 3 | Exercise retries, partial failure, idempotency, observability, and rollback | Failure-path tests, actionable metrics, rollout and recovery notes | Validation catches, false positives, rework |
| 4 | Compare the pilot with its baseline and tune roles, prompts, and checks | Team playbook, reusable templates, and an adoption decision | Cycle time, quality, reliability, cost per accepted change |

Ship these artifacts in the first month:

1. A current execution-path map with owners, dependencies, and known risks.
2. A baseline dashboard for delivery flow and service health.
3. A reviewed plan, PR review, and verification workflow using the scoped agents.
4. Focused regression and failure-path tests for the selected workflow.
5. A short team playbook stating where AI helps, where human approval is
   required, and which evidence closes a change.

Keep the pilot only if it reduces elapsed delivery time without increasing
rework, escaped defects, change failures, or recovery time. Treat an unavailable
cost or quality signal as unknown rather than zero.
