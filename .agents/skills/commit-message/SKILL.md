---
name: commit-message
description: Use when preparing or reviewing any Git commit message in this repository.
---

# Commit message

- Subject is at most 50 characters.
- Use an allowed conventional type.
- Capitalize the description after the type.
- Do not end the subject with a period.
- Use imperative mood: `Add`, `Fix`, `Remove`, `Refactor`.
- Add one blank line after the subject.
- Wrap body lines at 72 characters.
- Explain what changed and why.

Validate before committing:

```bash
python3 scripts/validate_commit_message.py .git/COMMIT_EDITMSG
```

Example:

```text
feat: Add task creation endpoint

Create a complete vertical slice so teams can reuse a tested API
pattern without copying product-specific code.
```
