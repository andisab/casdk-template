"""Tests for agents.utils.subagent_tracker.

Locks in:
- Hook return shape is the canonical empty dict (regression from {'continue_': True}).
- Agent/Task subagent-spawn tool is skipped on the main agent (logged elsewhere).
- Tool calls under an active subagent context are attributed to that subagent.
"""
import json
from pathlib import Path

import pytest

from agents.utils.subagent_tracker import SubagentTracker


class CapturingTranscript:
    def __init__(self) -> None:
        self.console: list[str] = []
        self.file: list[str] = []

    def write(self, text: str, end: str = "", flush: bool = True) -> None:
        self.console.append(text + end)

    def write_to_file(self, text: str, flush: bool = True) -> None:
        self.file.append(text)


@pytest.fixture
def tracker(session_dir: Path):
    t = SubagentTracker(transcript_writer=CapturingTranscript(), session_dir=session_dir)
    try:
        yield t
    finally:
        t.close()


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def test_register_subagent_spawn_returns_unique_ids_per_type(tracker):
    a = tracker.register_subagent_spawn(
        tool_use_id="t1", subagent_type="researcher", description="d", prompt="p"
    )
    b = tracker.register_subagent_spawn(
        tool_use_id="t2", subagent_type="researcher", description="d", prompt="p"
    )
    c = tracker.register_subagent_spawn(
        tool_use_id="t3", subagent_type="report-writer", description="d", prompt="p"
    )

    assert a == "RESEARCHER-1"
    assert b == "RESEARCHER-2"
    assert c == "REPORT-WRITER-1"


def test_register_subagent_spawn_truncates_long_prompts(tracker):
    long_prompt = "x" * 500
    tracker.register_subagent_spawn(
        tool_use_id="t1", subagent_type="researcher", description="d", prompt=long_prompt
    )

    preview = tracker.sessions["t1"].prompt_preview
    assert preview.endswith("...")
    assert len(preview) == 203  # 200 chars + "..."


def test_register_subagent_spawn_short_prompt_kept_verbatim(tracker):
    tracker.register_subagent_spawn(
        tool_use_id="t1", subagent_type="researcher", description="d", prompt="short"
    )
    assert tracker.sessions["t1"].prompt_preview == "short"


async def test_pre_tool_use_hook_returns_empty_dict(tracker):
    """Regression: canonical return is {}, not {'continue_': True}."""
    result = await tracker.pre_tool_use_hook(
        {"tool_name": "Read", "tool_input": {"file_path": "/x"}},
        "tu_main",
        None,
    )
    assert result == {}


async def test_post_tool_use_hook_returns_empty_dict_for_unknown_id(tracker):
    result = await tracker.post_tool_use_hook(
        {"tool_response": {}}, "never_seen", None
    )
    assert result == {}


async def test_post_tool_use_hook_returns_empty_dict_for_known_id(tracker):
    tracker.register_subagent_spawn(
        tool_use_id="tu_spawn", subagent_type="researcher", description="d", prompt="p"
    )
    tracker.set_current_context("tu_spawn")
    await tracker.pre_tool_use_hook(
        {"tool_name": "WebSearch", "tool_input": {"query": "x"}}, "tu_search", None
    )

    result = await tracker.post_tool_use_hook(
        {"tool_response": "ok"}, "tu_search", None
    )
    assert result == {}


async def test_pre_hook_skips_main_agent_subagent_spawn_tool(tracker, session_dir):
    """Agent/Task on the main agent is logged separately via register_subagent_spawn."""
    await tracker.pre_tool_use_hook(
        {"tool_name": "Agent", "tool_input": {"subagent_type": "researcher"}},
        "tu_a",
        None,
    )
    await tracker.pre_tool_use_hook(
        {"tool_name": "Task", "tool_input": {"subagent_type": "researcher"}},
        "tu_b",
        None,
    )

    assert _read_jsonl(session_dir / "tool_calls.jsonl") == []


async def test_pre_hook_logs_main_agent_normal_tool(tracker, session_dir):
    await tracker.pre_tool_use_hook(
        {"tool_name": "Read", "tool_input": {"file_path": "/x"}}, "tu_read", None
    )

    entries = _read_jsonl(session_dir / "tool_calls.jsonl")
    assert len(entries) == 1
    entry = entries[0]
    assert entry["agent_id"] == "MAIN_AGENT"
    assert entry["agent_type"] == "lead"
    assert entry["tool_name"] == "Read"
    assert entry["event"] == "tool_call_start"


async def test_pre_hook_attributes_tool_call_to_active_subagent(tracker, session_dir):
    sid = tracker.register_subagent_spawn(
        tool_use_id="tu_spawn",
        subagent_type="researcher",
        description="d",
        prompt="p",
    )
    tracker.set_current_context("tu_spawn")

    await tracker.pre_tool_use_hook(
        {"tool_name": "WebSearch", "tool_input": {"query": "x"}}, "tu_search", None
    )

    session = tracker.sessions["tu_spawn"]
    assert len(session.tool_calls) == 1
    assert session.tool_calls[0].tool_name == "WebSearch"

    entries = _read_jsonl(session_dir / "tool_calls.jsonl")
    assert len(entries) == 1
    assert entries[0]["agent_id"] == sid
    assert entries[0]["agent_type"] == "researcher"
    assert entries[0]["parent_tool_use_id"] == "tu_spawn"


async def test_post_hook_records_error_from_tool_response(tracker):
    tracker.register_subagent_spawn(
        tool_use_id="tu_spawn", subagent_type="researcher", description="d", prompt="p"
    )
    tracker.set_current_context("tu_spawn")
    await tracker.pre_tool_use_hook(
        {"tool_name": "WebSearch", "tool_input": {"query": "x"}}, "tu_search", None
    )

    await tracker.post_tool_use_hook(
        {"tool_response": {"error": "rate limit"}}, "tu_search", None
    )

    record = tracker.tool_call_records["tu_search"]
    assert record.error == "rate limit"
    assert record.tool_output == {"error": "rate limit"}


async def test_post_hook_writes_completion_entry_to_jsonl(tracker, session_dir):
    tracker.register_subagent_spawn(
        tool_use_id="tu_spawn", subagent_type="researcher", description="d", prompt="p"
    )
    tracker.set_current_context("tu_spawn")
    await tracker.pre_tool_use_hook(
        {"tool_name": "WebSearch", "tool_input": {"query": "x"}}, "tu_search", None
    )
    await tracker.post_tool_use_hook(
        {"tool_response": "result text"}, "tu_search", None
    )

    entries = _read_jsonl(session_dir / "tool_calls.jsonl")
    events = [e["event"] for e in entries]
    assert "tool_call_start" in events
    assert "tool_call_complete" in events

    completion = next(e for e in entries if e["event"] == "tool_call_complete")
    assert completion["success"] is True
    assert completion["tool_name"] == "WebSearch"


async def test_set_current_context_clears_when_set_to_none(tracker, session_dir):
    """Returning to main-agent context (no parent) should log under MAIN_AGENT again."""
    tracker.register_subagent_spawn(
        tool_use_id="tu_spawn", subagent_type="researcher", description="d", prompt="p"
    )
    tracker.set_current_context("tu_spawn")
    await tracker.pre_tool_use_hook(
        {"tool_name": "WebSearch", "tool_input": {"query": "x"}}, "tu_a", None
    )

    tracker.set_current_context(None)
    await tracker.pre_tool_use_hook(
        {"tool_name": "Read", "tool_input": {"file_path": "/y"}}, "tu_b", None
    )

    entries = _read_jsonl(session_dir / "tool_calls.jsonl")
    starts = [e for e in entries if e["event"] == "tool_call_start"]
    assert {e["agent_id"] for e in starts} == {"RESEARCHER-1", "MAIN_AGENT"}
