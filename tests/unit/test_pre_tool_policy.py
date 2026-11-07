import json
import subprocess
import sys
from pathlib import Path

import pytest

POLICY = Path(__file__).parents[2] / ".codex" / "hooks" / "pre_tool_use_policy.py"


def run_policy(command: str) -> str:
    result = subprocess.run(
        [sys.executable, str(POLICY)],
        input=json.dumps({"tool_input": {"command": command}}),
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def test_policy_blocks_embedded_secret() -> None:
    output = run_policy("API_KEY=sk-live-example ./deploy.sh")

    assert '"permissionDecision": "deny"' in output


@pytest.mark.parametrize(
    "command",
    [
        "git push --force origin main",
        "git push --force-with-lease origin main",
        "git push -f origin main",
        "git reset --hard HEAD~1",
    ],
)
def test_policy_blocks_destructive_git(command: str) -> None:
    assert '"permissionDecision": "deny"' in run_policy(command)


def test_policy_allows_local_verification() -> None:
    assert run_policy("make verify") == ""
