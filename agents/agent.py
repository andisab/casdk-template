"""Entry point for research agent using AgentDefinition for subagents."""

import asyncio
import os
from pathlib import Path

from claude_agent_sdk import (
    AgentDefinition,
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    HookMatcher,
    ResultMessage,
)
from dotenv import load_dotenv

from agents.utils.message_handler import process_assistant_message
from agents.utils.subagent_tracker import SubagentTracker
from agents.utils.transcript import TranscriptWriter, setup_session

# Load environment variables
load_dotenv()

# Paths to prompt files
PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_prompt(filename: str) -> str:
    """Load a prompt from the prompts directory."""
    prompt_path = PROMPTS_DIR / filename
    with open(prompt_path, encoding="utf-8") as f:
        return f.read().strip()


def build_agents(
    *, researcher_prompt: str, report_writer_prompt: str
) -> dict[str, AgentDefinition]:
    """Build the dict of subagent definitions used by this template.

    Exposed as a factory so tests can construct and inspect the AgentDefinitions
    without spinning up a ClaudeSDKClient.
    """
    return {
        "researcher": AgentDefinition(
            description=(
                "Use this agent when you need to gather research information on any topic. "
                "The researcher uses web search to find relevant information, articles, "
                "and sources from across the internet. Writes research findings to "
                "workspace/research-notes/ for later use by report writers. Ideal for "
                "complex research tasks that require deep searching and cross-referencing."
            ),
            tools=["WebSearch", "Write"],
            prompt=researcher_prompt,
            model="haiku",
            # Cap iterations so a confused researcher can't burn through
            # WebSearch calls indefinitely.
            maxTurns=10,
        ),
        "report-writer": AgentDefinition(
            description=(
                "Use this agent when you need to create a formal research report document. "
                "The report-writer reads research findings from workspace/research-notes/ "
                "and synthesizes them into clear, concise, professionally formatted reports "
                "in workspace/results/. Ideal for creating structured documents with proper "
                "citations and organization. Does NOT conduct web searches - only reads "
                "existing research notes and creates reports."
            ),
            tools=["Skill", "Write", "Glob", "Read"],
            prompt=report_writer_prompt,
            model="haiku",
            # Subagents do not inherit project skills automatically - declare them here.
            # joplin-research routes by request type; it delegates markdown formatting
            # to joplin-formatting, which must be available to the same subagent.
            skills=["joplin-research", "joplin-formatting"],
            maxTurns=5,
        ),
    }


def build_options(
    *,
    system_prompt: str,
    agents: dict[str, AgentDefinition],
    hooks: dict[str, list[HookMatcher]] | None = None,
) -> ClaudeAgentOptions:
    """Build the ClaudeAgentOptions for the lead agent session.

    Exposed as a factory so tests can assert on the constructed options without
    starting a session.
    """
    return ClaudeAgentOptions(
        permission_mode="bypassPermissions",
        setting_sources=["project"],  # Load skills from project .claude directory
        system_prompt=system_prompt,
        # The subagent tool was renamed Task -> Agent in Claude Code v2.1.63.
        # Allow both so the lead agent can spawn subagents on old and new SDKs.
        allowed_tools=["Agent", "Task"],
        agents=agents,
        hooks=hooks or {},
        model="haiku",
    )


async def chat():
    """Start interactive chat with the research agent."""

    # Check API key first, before creating any files
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("\nError: ANTHROPIC_API_KEY not found.")
        print("Set it in a .env file or export it in your shell.")
        print("Get your key at: https://console.anthropic.com/settings/keys\n")
        return

    # Setup session directory and transcript
    transcript_file, session_dir = setup_session()

    # Create transcript writer
    transcript = TranscriptWriter(transcript_file)

    # Load prompts
    lead_agent_prompt = load_prompt("lead_agent.txt")
    researcher_prompt = load_prompt("researcher.txt")
    report_writer_prompt = load_prompt("report_writer.txt")

    # Initialize subagent tracker with transcript writer and session directory
    tracker = SubagentTracker(transcript_writer=transcript, session_dir=session_dir)

    # Define specialized subagents
    agents = build_agents(
        researcher_prompt=researcher_prompt,
        report_writer_prompt=report_writer_prompt,
    )

    # Set up hooks for tracking (matcher=None matches all tools)
    hooks: dict[str, list[HookMatcher]] = {
        "PreToolUse": [HookMatcher(matcher=None, hooks=[tracker.pre_tool_use_hook])],
        "PostToolUse": [HookMatcher(matcher=None, hooks=[tracker.post_tool_use_hook])],
    }

    options = build_options(
        system_prompt=lead_agent_prompt,
        agents=agents,
        hooks=hooks,
    )

    print("\n=== Research Agent ===")
    print("Ask me to research any topic, gather information, or analyze documents.")
    print("I can delegate complex tasks to specialized researcher and report-writer agents.")
    print(f"\nRegistered subagents: {', '.join(agents.keys())}")
    print(f"Session logs: {session_dir}")
    print("Type 'exit' or 'quit' to end.\n")

    # Cumulative session metrics, populated from ResultMessage events.
    totals = {"turns": 0, "cost_usd": 0.0, "input_tokens": 0, "output_tokens": 0}

    try:
        async with ClaudeSDKClient(options=options) as client:
            while True:
                # Get input
                try:
                    user_input = input("\nYou: ").strip()
                except (EOFError, KeyboardInterrupt):
                    break

                if not user_input or user_input.lower() in ["exit", "quit", "q"]:
                    break

                # Write user input to transcript (file only, not console)
                transcript.write_to_file(f"\nYou: {user_input}\n")

                # Send to agent
                await client.query(prompt=user_input)

                transcript.write("\nAgent: ", end="")

                # Stream and process response
                async for msg in client.receive_response():
                    if isinstance(msg, AssistantMessage):
                        process_assistant_message(msg, tracker, transcript)
                    elif isinstance(msg, ResultMessage):
                        _accumulate_result(totals, msg)

                transcript.write("\n")
    finally:
        transcript.write("\n\nGoodbye!\n")
        if totals["turns"]:
            transcript.write(_format_totals(totals) + "\n")
        transcript.close()
        tracker.close()
        print(f"\nSession logs saved to: {session_dir}")
        print(f"  - Transcript: {transcript_file}")
        print(f"  - Tool calls: {session_dir / 'tool_calls.jsonl'}")


def _accumulate_result(totals: dict, msg: ResultMessage) -> None:
    """Add a ResultMessage's metrics into the running session totals dict."""
    totals["turns"] += getattr(msg, "num_turns", 0) or 0
    cost = getattr(msg, "total_cost_usd", None)
    if cost is not None:
        totals["cost_usd"] += cost
    usage = getattr(msg, "usage", None) or {}
    totals["input_tokens"] += usage.get("input_tokens", 0) or 0
    totals["output_tokens"] += usage.get("output_tokens", 0) or 0


def _format_totals(totals: dict) -> str:
    """Render the cumulative session totals as a single-line summary."""
    return (
        f"Session: {totals['turns']} turns, "
        f"${totals['cost_usd']:.4f} USD, "
        f"{totals['input_tokens']:,} input / {totals['output_tokens']:,} output tokens"
    )


if __name__ == "__main__":
    asyncio.run(chat())
