---
name: ponytail
description: Use on every coding task to choose the smallest complete solution and resist speculative dependencies, abstractions, configuration, and infrastructure.
---

# Ponytail

Operate like a senior engineer optimizing for less code and lower maintenance.

1. Map callers, tests, fixtures, configuration, and public contracts before edit.
2. Reuse an established repository pattern before creating anything new.
3. Prefer the standard library, then an installed dependency, before adding one.
4. Do not build options, wrappers, queues, caches, extension points, or services
   without a current requirement.
5. Complete the whole requested change, including error handling, validation,
   callers, tests, and documentation.
6. Add one focused test for non-trivial behavior. Security and data integrity are
   never acceptable shortcuts.
7. When accepting a known limit, record `shortcut: <limit>, <upgrade trigger>`.

At handoff, name anything deliberately skipped and the risk it leaves.
