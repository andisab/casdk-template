"""Tests for agents.utils.message_handler.

These tests lock in the Task -> Agent rename compatibility (Claude Code v2.1.63)
and verify that block dispatch, parent context propagation, and subagent
spawn detection behave correctly.
"""

from typing import Any

from claude_agent_sdk import AssistantMessage, TextBlock, ToolUseBlock

from agents.utils.message_handler import SUBAGENT_SPAWN_TOOLS, process_assistant_message


class FakeTracker:
    def __init__(self) -> None:
        self.parent_id_history: list[Any] = []
        self.spawns: list[dict[str, Any]] = []

    def set_current_context(self, parent_tool_use_id: Any) -> None:
        self.parent_id_history.append(parent_tool_use_id)

    def register_subagent_spawn(
        self, *, tool_use_id: str, subagent_type: str, description: str, prompt: str
    ) -> str:
        sid = f"{subagent_type.upper()}-{len(self.spawns) + 1}"
        self.spawns.append(
            {
                "tool_use_id": tool_use_id,
                "subagent_type": subagent_type,
                "description": description,
                "prompt": prompt,
                "subagent_id": sid,
            }
        )
        return sid


class FakeTranscript:
    def __init__(self) -> None:
        self.console: list[str] = []
        self.tool_used = False
        self.flushes = 0

    def write(self, text: str, end: str = "", flush: bool = True) -> None:
        self.console.append(text + end)

    def write_to_file(self, text: str, flush: bool = True) -> None:  # pragma: no cover
        pass

    def mark_tool_used(self) -> None:
        self.tool_used = True

    def flush_pending_break(self) -> None:
        if self.tool_used:
            self.console.append("\n")
            self.tool_used = False
            self.flushes += 1


def _msg(*blocks, parent_tool_use_id: str | None = None) -> AssistantMessage:
    return AssistantMessage(
        content=list(blocks), model="haiku", parent_tool_use_id=parent_tool_use_id
    )


def test_subagent_spawn_tools_constant_includes_both_names():
    """Regression: SDK renamed Task -> Agent in Claude Code v2.1.63 — match both."""
    assert "Agent" in SUBAGENT_SPAWN_TOOLS
    assert "Task" in SUBAGENT_SPAWN_TOOLS


def test_text_block_writes_text_to_transcript():
    tracker, transcript = FakeTracker(), FakeTranscript()
    process_assistant_message(_msg(TextBlock(text="hello world")), tracker, transcript)
    assert "".join(transcript.console) == "hello world"


def test_parent_tool_use_id_propagates_to_tracker():
    tracker, transcript = FakeTracker(), FakeTranscript()
    process_assistant_message(
        _msg(TextBlock(text="x"), parent_tool_use_id="tu_42"), tracker, transcript
    )
    assert tracker.parent_id_history == ["tu_42"]


def test_agent_tool_block_triggers_subagent_spawn():
    """Current SDK emits 'Agent' for subagent invocations."""
    tracker, transcript = FakeTracker(), FakeTranscript()
    block = ToolUseBlock(
        id="tu_1",
        name="Agent",
        input={
            "subagent_type": "researcher",
            "description": "Find quantum hardware updates",
            "prompt": "Research recent qubit advances...",
        },
    )

    process_assistant_message(_msg(block), tracker, transcript)

    assert len(tracker.spawns) == 1
    assert tracker.spawns[0]["subagent_type"] == "researcher"
    assert tracker.spawns[0]["tool_use_id"] == "tu_1"
    assert "RESEARCHER-1" in "".join(transcript.console)


def test_legacy_task_tool_block_still_triggers_spawn():
    """Older Claude Code builds (<v2.1.63) emit 'Task' instead of 'Agent'."""
    tracker, transcript = FakeTracker(), FakeTranscript()
    block = ToolUseBlock(
        id="tu_legacy",
        name="Task",
        input={"subagent_type": "report-writer", "description": "synth", "prompt": "go"},
    )

    process_assistant_message(_msg(block), tracker, transcript)

    assert len(tracker.spawns) == 1
    assert tracker.spawns[0]["subagent_type"] == "report-writer"


def test_other_tool_blocks_do_not_trigger_spawn():
    tracker, transcript = FakeTracker(), FakeTranscript()
    block = ToolUseBlock(id="tu_2", name="WebSearch", input={"query": "foo"})

    process_assistant_message(_msg(block), tracker, transcript)

    assert tracker.spawns == []


def test_missing_subagent_input_fields_use_defaults():
    tracker, transcript = FakeTracker(), FakeTranscript()
    block = ToolUseBlock(id="tu_3", name="Agent", input={})

    process_assistant_message(_msg(block), tracker, transcript)

    assert tracker.spawns[0]["subagent_type"] == "unknown"
    assert tracker.spawns[0]["description"] == "no description"
    assert tracker.spawns[0]["prompt"] == ""


def test_tool_use_then_text_flushes_break_separator():
    """A ToolUseBlock should mark a pending break; the next TextBlock flushes it.

    Replaces the implicit-global-state behavior with explicit transcript state.
    """
    tracker, transcript = FakeTracker(), FakeTranscript()

    process_assistant_message(
        _msg(ToolUseBlock(id="tu_a", name="WebSearch", input={"query": "x"})),
        tracker,
        transcript,
    )
    assert transcript.tool_used is True
    assert transcript.flushes == 0

    process_assistant_message(_msg(TextBlock(text="next")), tracker, transcript)
    assert transcript.flushes == 1
    assert transcript.tool_used is False


def test_mixed_blocks_in_one_message():
    """A single AssistantMessage may contain text + tool use + text."""
    tracker, transcript = FakeTracker(), FakeTranscript()
    msg = _msg(
        TextBlock(text="thinking..."),
        ToolUseBlock(
            id="tu_x",
            name="Agent",
            input={"subagent_type": "researcher", "description": "d", "prompt": "p"},
        ),
        TextBlock(text="done"),
    )

    process_assistant_message(msg, tracker, transcript)

    assert len(tracker.spawns) == 1
    output = "".join(transcript.console)
    assert "thinking..." in output
    assert "RESEARCHER-1" in output
    assert "done" in output
