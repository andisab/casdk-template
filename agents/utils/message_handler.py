"""Message handling for processing agent responses."""

from typing import Any

from claude_agent_sdk import TextBlock, ToolUseBlock


# The subagent tool was renamed Task -> Agent in Claude Code v2.1.63.
# Match both so detection works on old and new SDK builds.
SUBAGENT_SPAWN_TOOLS = ("Agent", "Task")


# Track if a tool was just used (for formatting)
_tool_just_used = False


def process_assistant_message(msg: Any, tracker: Any, transcript: Any) -> None:
    """Process an AssistantMessage and write output to transcript.

    Args:
        msg: AssistantMessage to process
        tracker: SubagentTracker instance
        transcript: TranscriptWriter instance
    """
    global _tool_just_used

    # Update tracker context with parent_tool_use_id from message
    parent_id = getattr(msg, 'parent_tool_use_id', None)
    tracker.set_current_context(parent_id)

    for block in msg.content:
        if isinstance(block, TextBlock):
            # Add newline if a tool was just used
            if _tool_just_used:
                transcript.write("\n", end="")
                _tool_just_used = False
            transcript.write(block.text, end="")

        elif isinstance(block, ToolUseBlock):
            # Mark that a tool was used
            _tool_just_used = True

            # Only handle subagent spawn tool (Agent / Task)
            if block.name in SUBAGENT_SPAWN_TOOLS:
                subagent_type = block.input.get('subagent_type', 'unknown')
                description = block.input.get('description', 'no description')
                prompt = block.input.get('prompt', '')

                # Register with tracker and get the subagent ID
                subagent_id = tracker.register_subagent_spawn(
                    tool_use_id=block.id,
                    subagent_type=subagent_type,
                    description=description,
                    prompt=prompt
                )

                # User-facing output with subagent ID
                transcript.write(f"\n\n[🚀 Spawning {subagent_id}: {description}]\n", end="")
