
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_cli(*arguments):
    return subprocess.run(
        [sys.executable, "ask.py", *arguments],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=15
    )


def test_basic_dry_run():
    result = run_cli(
        "Explain RAG",
        "--dry-run"
    )

    assert result.returncode == 0
    assert "Explain RAG" in result.stdout
    assert "No API requests were made" in result.stdout


def test_streaming_dry_run():
    result = run_cli(
        "Explain AI agents",
        "--stream",
        "--dry-run"
    )

    assert result.returncode == 0
    assert "Streaming: Enabled" in result.stdout
    assert "No API requests were made" in result.stdout


def test_system_prompt():
    result = run_cli(
        "Explain embeddings",
        "--system",
        "You are an AI instructor",
        "--dry-run"
    )

    assert result.returncode == 0
    assert "You are an AI instructor" in result.stdout


def test_missing_prompt():
    result = run_cli("--dry-run")

    assert result.returncode != 0
