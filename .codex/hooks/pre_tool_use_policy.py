#!/usr/bin/env python3
"""Deny known secret exposure and destructive delivery commands."""

from __future__ import annotations

import json
import re
import sys

RULES: tuple[tuple[re.Pattern[str], str], ...] = (
    (
        re.compile(r"(?:^|\s)(?:sk-live-|sk-prod-|API_KEY=\S+)", re.IGNORECASE),
        "A credential-like value must not be embedded in a shell command.",
    ),
    (
        re.compile(
            r"\bgit\s+(?:push\b[^\n]*(?:--force(?:-with-lease)?\b|\s-f(?:\s|$))"
            r"|reset\s+--hard|clean\s+-[a-z]*f)",
            re.IGNORECASE,
        ),
        "Destructive or forceful Git operations are blocked.",
    ),
    (
        re.compile(r"\bgh\s+pr\s+(?:merge|ready)\b", re.IGNORECASE),
        "Agents must not merge or mark pull requests ready.",
    ),
    (
        re.compile(r"\bdocker\s+push\b", re.IGNORECASE),
        "Publishing container images requires separate human authorization.",
    ),
    (
        re.compile(
            r"\b(?:kubectl\s+(?:apply|delete)|terraform\s+(?:apply|destroy))\b",
            re.IGNORECASE,
        ),
        "Cloud or cluster mutation requires separate human authorization.",
    ),
    (
        re.compile(r"\balembic\s+downgrade\b", re.IGNORECASE),
        "Automatic database downgrades are blocked.",
    ),
    (
        re.compile(
            r"\b(?:deploy-production|publish-image|ENV=(?:prod|production))\b",
            re.IGNORECASE,
        ),
        "Production execution requires a separate human-controlled workflow.",
    ),
    (
        re.compile(r"\brm\s+-[a-z]*r[a-z]*f[a-z]*\s+(?:/|~|\$HOME)(?:\s|$)", re.IGNORECASE),
        "Broad recursive deletion is blocked.",
    ),
)


def violation(command: str) -> str | None:
    for pattern, reason in RULES:
        if pattern.search(command):
            return reason
    return None


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return 0

    command = event.get("tool_input", {}).get("command")
    if not isinstance(command, str):
        return 0

    reason = violation(command)
    if reason:
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": reason,
                    }
                }
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
