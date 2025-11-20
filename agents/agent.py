"""Entry point for research agent using AgentDefinition for subagents."""

import asyncio
import os
import subprocess
import shutil
from pathlib import Path
from dotenv import load_dotenv
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AgentDefinition, HookMatcher

from agents.utils.subagent_tracker import SubagentTracker
from agents.utils.transcript import setup_session, TranscriptWriter
from agents.utils.message_handler import process_assistant_message

# Load environment variables
load_dotenv()

# Paths to prompt files
PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_prompt(filename: str) -> str:
    """Load a prompt from the prompts directory."""
    prompt_path = PROMPTS_DIR / filename
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def find_claude_cli() -> str | None:
    """Find the Claude CLI executable.

    Tries multiple approaches:
    1. Check if 'claude' is in PATH
    2. Check npm global bin directory
    3. Check common nvm installation paths

    Returns:
        Path to claude executable, or None if not found
    """
    # First, try shutil.which (checks PATH)
    claude_path = shutil.which("claude")
    if claude_path:
        return claude_path

    # Try npm global bin directory
    try:
        npm_prefix = subprocess.run(
            ["npm", "config", "get", "prefix"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5
        ).stdout.strip()

        npm_bin_claude = Path(npm_prefix) / "bin" / "claude"
        if npm_bin_claude.exists():
            return str(npm_bin_claude)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Check common nvm paths as fallback
    home = Path.home()
    nvm_paths = [
        home / ".nvm" / "versions" / "node",
        home / ".local" / "share" / "nvm",
    ]

    for nvm_base in nvm_paths:
        if nvm_base.exists():
            # Find the most recent node version
            try:
                node_versions = sorted(nvm_base.iterdir(), reverse=True)
                for version_dir in node_versions:
                    claude_bin = version_dir / "bin" / "claude"
                    if claude_bin.exists():
                        return str(claude_bin)
            except (OSError, PermissionError):
                continue

    return None


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
    agents = {
        "researcher": AgentDefinition(
            description=(
                "Use this agent when you need to gather research information on any topic. "
                "The researcher uses web search to find relevant information, articles, and sources "
                "from across the internet. Writes research findings to workspace/research-notes/ "
                "for later use by report writers. Ideal for complex research tasks "
                "that require deep searching and cross-referencing."
            ),
            tools=["WebSearch", "Write"],
            prompt=researcher_prompt,
            model="haiku"
        ),
        "report-writer": AgentDefinition(
            description=(
                "Use this agent when you need to create a formal research report document. "
                "The report-writer reads research findings from workspace/research-notes/ and synthesizes "
                "them into clear, concise, professionally formatted reports in workspace/results/. "
                "Ideal for creating structured documents with proper citations and organization. "
                "Does NOT conduct web searches - only reads existing research notes and creates reports."
            ),
            tools=["Skill", "Write", "Glob", "Read"],
            prompt=report_writer_prompt,
            model="haiku"
        )
    }

    # Set up hooks for tracking
    hooks = {
        'PreToolUse': [
            HookMatcher(
                matcher=None,  # Match all tools
                hooks=[tracker.pre_tool_use_hook]
            )
        ],
        'PostToolUse': [
            HookMatcher(
                matcher=None,  # Match all tools
                hooks=[tracker.post_tool_use_hook]
            )
        ]
    }

    # Find Claude CLI executable
    claude_cli_path = find_claude_cli()
    if not claude_cli_path:
        print("\n❌ Error: Could not find Claude CLI executable")
        print("\nPlease install Claude Code:")
        print("  npm install -g @anthropic-ai/claude-code")
        print("\nOr ensure it's in your PATH:")
        print("  export PATH=\"$(npm config get prefix)/bin:$PATH\"")
        return

    # Add the npm bin directory to PATH so node can be found
    # Claude CLI is a Node.js script that requires node in PATH
    claude_bin_dir = Path(claude_cli_path).parent
    current_path = os.environ.get("PATH", "")
    if str(claude_bin_dir) not in current_path:
        os.environ["PATH"] = f"{claude_bin_dir}:{current_path}"

    options = ClaudeAgentOptions(
        permission_mode="bypassPermissions",
        setting_sources=["project"],  # Load skills from project .claude directory
        system_prompt=lead_agent_prompt,
        allowed_tools=["Task"],
        agents=agents,
        hooks=hooks,
        model="haiku",
        cli_path=claude_cli_path
    )

    print("\n=== Research Agent ===")
    print("Ask me to research any topic, gather information, or analyze documents.")
    print("I can delegate complex tasks to specialized researcher and report-writer agents.")
    print(f"\nRegistered subagents: {', '.join(agents.keys())}")
    print(f"Session logs: {session_dir}")
    print("Type 'exit' or 'quit' to end.\n")

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
                    if type(msg).__name__ == 'AssistantMessage':
                        process_assistant_message(msg, tracker, transcript)

                transcript.write("\n")
    finally:
        transcript.write("\n\nGoodbye!\n")
        transcript.close()
        tracker.close()
        print(f"\nSession logs saved to: {session_dir}")
        print(f"  - Transcript: {transcript_file}")
        print(f"  - Tool calls: {session_dir / 'tool_calls.jsonl'}")


if __name__ == "__main__":
    asyncio.run(chat())
