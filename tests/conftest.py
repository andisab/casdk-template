"""Shared pytest fixtures."""
from pathlib import Path

import pytest

from agents.utils import message_handler


@pytest.fixture
def tmp_cwd(monkeypatch, tmp_path: Path) -> Path:
    """Run the test with cwd set to tmp_path so logs/ etc. land in isolation."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture
def session_dir(tmp_path: Path) -> Path:
    """A pre-created session directory for tracker fixtures."""
    d = tmp_path / "session_test"
    d.mkdir()
    return d


@pytest.fixture
def transcript_file(session_dir: Path) -> Path:
    return session_dir / "transcript.txt"


@pytest.fixture(autouse=True)
def _reset_message_handler_state():
    """Reset module-level _tool_just_used between tests so state never leaks across cases."""
    message_handler._tool_just_used = False
    yield
    message_handler._tool_just_used = False
