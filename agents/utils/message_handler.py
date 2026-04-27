"""Message handling for processing agent responses.

Dispatches blocks from a streamed ``AssistantMessage`` to the transcript
writer and to the subagent tracker. Inter-message formatting state (the
"a tool was just used; emit a newline before the next text" flag) lives
on ``TranscriptWriter`` rather than at module scope, so tests don't need
to reset it between cases.

The tracker and transcript dependencies are typed as ``Protocol``s so that
test fakes don't need to inherit from the concrete classes.
"""

from __future__ import annotations

from typing import Protocol

from claude_agent_sdk import AssistantMessage, TextBlock, ToolUseBlock

# The subagent tool was renamed Task -> Agent in Claude Code v2.1.63.
# Match both so detection works on old and new SDK builds.
SUBAGENT_SPAWN_TOOLS: tuple[str, ...] = ("Agent", "Task")


class _Tracker(Protocol):
    def set_current_context(self, parent_tool_use_id: str | None) -> None: ...

    def register_subagent_spawn(
        self,
        *,
        tool_use_id: str,
        subagent_type: str,
        description: str,
        prompt: str,
    ) -> str: ...


class _Transcript(Protocol):
    def write(self, text: str, end: str = ..., flush: bool = ...) -> None: ...

    def mark_tool_used(self) -> None: ...

    def flush_pending_break(self) -> None: ...


def process_assistant_message(
    msg: AssistantMessage,
    tracker: _Tracker,
    transcript: _Transcript,
) -> None:
    """Process an AssistantMessage and write output to transcript."""
    parent_id = getattr(msg, "parent_tool_use_id", None)
    tracker.set_current_context(parent_id)

    for block in msg.content:
        if isinstance(block, TextBlock):
            transcript.flush_pending_break()
            transcript.write(block.text, end="")

        elif isinstance(block, ToolUseBlock):
            transcript.mark_tool_used()

            # Only handle the subagent-spawn tool here; other tool calls are
            # logged via the PreToolUse hook on the tracker.
            if block.name in SUBAGENT_SPAWN_TOOLS:
                subagent_type = block.input.get("subagent_type", "unknown")
                description = block.input.get("description", "no description")
                prompt = block.input.get("prompt", "")

                subagent_id = tracker.register_subagent_spawn(
                    tool_use_id=block.id,
                    subagent_type=subagent_type,
                    description=description,
                    prompt=prompt,
                )

                transcript.write(f"\n\n[🚀 Spawning {subagent_id}: {description}]\n", end="")
