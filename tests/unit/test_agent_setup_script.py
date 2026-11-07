from __future__ import annotations

import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "setup_agent_tools.sh"


def test_agent_setup_help_lists_safe_modes() -> None:
    result = subprocess.run(
        ["/bin/bash", str(SCRIPT), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "--check" in result.stdout
    assert "--all" in result.stdout
    assert "--yes" in result.stdout


def test_agent_setup_check_warns_without_clients(tmp_path: Path) -> None:
    environment = os.environ.copy()
    environment.update(
        {
            "PATH": "/usr/bin:/bin",
            "HOME": str(tmp_path),
            "CODEX_HOME": str(tmp_path / ".codex"),
        }
    )

    result = subprocess.run(
        ["/bin/bash", str(SCRIPT), "--check", "--all"],
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )

    assert result.returncode == 1
    assert "Claude Code CLI: missing" in result.stdout
    assert "Codex CLI: missing" in result.stdout
    assert "CodeGraph CLI: missing" in result.stdout
