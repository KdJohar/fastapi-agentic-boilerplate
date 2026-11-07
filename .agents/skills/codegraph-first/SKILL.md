---
name: codegraph-first
description: Use before broad search, planning, editing, debugging, or reviewing code when a local .codegraph index is available.
---

# CodeGraph first

1. Ask one focused question naming the feature, symbol, or execution path.
2. Request the route, view, controller, helper, model/schema, and tests together.
3. Treat returned source as already read; do not immediately re-open every file.
4. Use raw `rg` only for gaps the graph cannot answer.
5. Before editing a shared symbol, inspect its callers and blast radius.
6. The index is discovery evidence, not proof of runtime or production state.

Example query:

```text
Trace task creation from HTTP route through transaction and persistence, including
error handling and tests. Show callers and the blast radius of TaskCreate.
```

Initialise and refresh the local, ignored index only when needed:

```bash
codegraph init
codegraph sync
```
