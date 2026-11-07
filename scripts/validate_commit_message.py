#!/usr/bin/env python3
"""Validate repository commit-message conventions."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

SUBJECT = re.compile(
    r"^(?P<type>feat|fix|docs|test|refactor|perf|build|ci|chore)"
    r"(?:\([a-z0-9._-]+\))?!?: (?P<description>.+)$"
)
NON_IMPERATIVE_STARTS = {
    "Added",
    "Adds",
    "Changed",
    "Changes",
    "Created",
    "Creates",
    "Fixed",
    "Fixes",
    "Implemented",
    "Implements",
    "Refactored",
    "Refactors",
    "Removed",
    "Removes",
    "Updated",
    "Updates",
}


def validate(message: str) -> list[str]:
    lines = message.rstrip("\n").splitlines()
    if not lines or not lines[0].strip():
        return ["subject must not be empty"]

    errors: list[str] = []
    subject = lines[0]
    if len(subject) > 50:
        errors.append(f"subject is {len(subject)} characters; maximum is 50")
    if subject.endswith("."):
        errors.append("subject must not end with a period")

    match = SUBJECT.fullmatch(subject)
    if match is None:
        errors.append("subject must use '<type>: Capitalized imperative description'")
    else:
        description = match.group("description")
        if not description[0].isupper():
            errors.append("description after the type must start with a capital letter")
        first_word = description.split(maxsplit=1)[0]
        if first_word in NON_IMPERATIVE_STARTS:
            errors.append("subject must use imperative mood, such as 'Add' or 'Fix'")

    has_separator = len(lines) >= 2 and lines[1] == ""
    if not has_separator:
        errors.append("subject and body must be separated by one blank line")

    body = lines[2:] if has_separator else lines[1:]
    if not any(line.strip() for line in body):
        errors.append("body must explain what changed and why")
    body_start = 3 if has_separator else 2
    for line_number, line in enumerate(body, start=body_start):
        if len(line) > 72:
            errors.append(f"body line {line_number} is {len(line)} characters; maximum is 72")
    return errors


def messages_in_range(revision_range: str) -> list[tuple[str, str]]:
    commits = subprocess.run(
        ["git", "rev-list", "--reverse", revision_range],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    return [
        (
            commit,
            subprocess.run(
                ["git", "show", "-s", "--format=%B", commit],
                check=True,
                capture_output=True,
                text=True,
            ).stdout,
        )
        for commit in commits
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("message_file", nargs="?", type=Path)
    parser.add_argument("--range", dest="revision_range")
    args = parser.parse_args()

    if bool(args.message_file) == bool(args.revision_range):
        parser.error("provide exactly one message file or --range")

    messages = (
        messages_in_range(args.revision_range)
        if args.revision_range
        else [(str(args.message_file), args.message_file.read_text(encoding="utf-8"))]
    )

    failed = False
    for identifier, message in messages:
        errors = validate(message)
        if errors:
            failed = True
            print(f"Invalid commit message ({identifier}):", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
