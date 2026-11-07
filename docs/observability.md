# Observability

## Runtime signals

The service exposes low-cardinality Prometheus metrics at `/metrics`:

- `http_requests_total{method,route,status}`
- `http_request_duration_seconds{method,route}`

Use p50 to understand normal experience and p95/p99 to see tail latency. Alert on
user-impacting symptoms—sustained error rate, latency, or readiness failure—rather
than isolated exceptions.

JSON logs include timestamp, level, logger, message, and request ID. Never add
payloads, tokens, personal data, raw SQL parameters, or secrets. Propagate the
request ID into outbound calls when another service supports correlation.

## Next signals by evidence

Add database pool saturation and query latency when the deployment has a stable
global connection budget. Add queue depth and oldest-message age when asynchronous
work exists. Add business outcome counters only when their definitions are durable
and actionable.

Avoid user IDs, raw URLs, exception strings, or arbitrary payload values in metric
labels; they create cardinality and privacy risk.

## Delivery and AI evaluation

Keep delivery metrics separate from runtime metrics. Review them as team trends:

- Cycle and review wait time
- First-pass CI and flake rate
- Deployment frequency and lead time
- Change failure and recovery time
- Escaped defects and rollback
- AI plan revisions, review precision, validation catches, rework, time, and cost

State whether cost data is billed, estimated, or incomplete. Missing data is
unknown, not zero.
