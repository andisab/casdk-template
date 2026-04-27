#!/usr/bin/env python3
"""Analyze tool call logs from research agent sessions."""

from __future__ import annotations

import argparse
import json
import logging
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def analyze_session(session_dir: Path) -> dict[str, Any] | None:
    """Analyze a single session's tool call logs.

    Returns ``None`` when the session has no ``tool_calls.jsonl`` or when the
    file is empty. Malformed JSONL lines are logged at WARNING level and
    skipped (rather than silently dropped) so log corruption is visible.
    """
    tool_log = session_dir / "tool_calls.jsonl"

    if not tool_log.exists():
        return None

    tool_calls: list[dict[str, Any]] = []
    with open(tool_log, encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                tool_calls.append(json.loads(line))
            except json.JSONDecodeError as exc:
                logger.warning("Skipping malformed JSONL line %d in %s: %s", lineno, tool_log, exc)

    if not tool_calls:
        return None

    agents: set[str] = set()
    tools_by_agent: dict[str, list[str]] = defaultdict(list)
    tool_counts: Counter[str] = Counter()
    errors: list[dict[str, Any]] = []

    for call in tool_calls:
        if call.get("event") == "tool_call_start":
            agent_id = call.get("agent_id", "UNKNOWN")
            tool_name = call.get("tool_name", "UNKNOWN")

            agents.add(agent_id)
            tools_by_agent[agent_id].append(tool_name)
            tool_counts[tool_name] += 1

        elif call.get("event") == "tool_call_complete":
            if not call.get("success", True):
                errors.append(
                    {
                        "agent": call.get("agent_id"),
                        "tool": call.get("tool_name"),
                        "error": call.get("error"),
                    }
                )

    session_name = session_dir.name
    timestamp_str = session_name.replace("session_", "")
    try:
        session_time = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
        session_time_formatted = session_time.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        session_time_formatted = timestamp_str

    return {
        "session_dir": session_dir,
        "session_time": session_time_formatted,
        "agents": sorted(agents),
        "tools_by_agent": dict(tools_by_agent),
        "tool_counts": dict(tool_counts),
        "total_calls": sum(1 for c in tool_calls if c.get("event") == "tool_call_start"),
        "errors": errors,
    }


def print_session_summary(stats: dict[str, Any]) -> None:
    """Print a human-readable summary of session statistics."""
    print(f"\n{'=' * 70}")
    print(f"Session: {stats['session_dir'].name}")
    print(f"Time: {stats['session_time']}")
    print(f"{'=' * 70}\n")

    print(f"Agents: {', '.join(stats['agents'])}")
    print(f"Total tool calls: {stats['total_calls']}\n")

    print("Tool Usage:")
    for tool, count in sorted(stats["tool_counts"].items(), key=lambda x: -x[1]):
        print(f"  {tool:20s} {count:3d} calls")

    if stats["errors"]:
        print(f"\nErrors: {len(stats['errors'])}")
        for err in stats["errors"][:5]:
            print(f"  - [{err['agent']}] {err['tool']}: {err['error']}")

    print("\nTool Calls by Agent:")
    for agent, tools in sorted(stats["tools_by_agent"].items()):
        tool_summary = Counter(tools)
        print(f"\n  {agent}:")
        for tool, count in sorted(tool_summary.items(), key=lambda x: -x[1]):
            print(f"    {tool:18s} {count:3d}x")


def _resolve_session(logs_dir: Path, name: str) -> Path:
    """Resolve a session name (or path) to an absolute session directory."""
    return logs_dir / name if "/" not in name else Path(name)


def main() -> None:
    """CLI entry point."""
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(
        description="Analyze tool-call logs from a research-agent session.",
    )
    parser.add_argument(
        "session",
        nargs="?",
        help=(
            "Session directory name (e.g. session_20260101_120000) or path. "
            "Defaults to the most recent session under logs/."
        ),
    )
    args = parser.parse_args()

    logs_dir = Path("logs")
    if not logs_dir.exists():
        print("No logs directory found.")
        return

    sessions = sorted(
        (d for d in logs_dir.iterdir() if d.is_dir() and d.name.startswith("session_")),
        key=lambda x: x.name,
        reverse=True,
    )

    if not sessions:
        print("No session logs found.")
        return

    if args.session:
        session_path = _resolve_session(logs_dir, args.session)
        if not session_path.exists():
            print(f"Error: Session not found: {session_path}")
            return

        stats = analyze_session(session_path)
        if stats:
            print_session_summary(stats)
        else:
            print(f"No tool call data found in {session_path}")
        return

    print("\n=== Research Agent Log Analysis ===\n")
    print(f"Found {len(sessions)} session(s)\n")

    recent_session = sessions[0]
    print(f"Analyzing most recent session: {recent_session.name}")

    stats = analyze_session(recent_session)
    if stats:
        print_session_summary(stats)
    else:
        print("No tool call data found in most recent session.")

    if len(sessions) > 1:
        print(f"\n{'=' * 70}")
        print(f"\nOther sessions ({len(sessions) - 1}):")
        for session in sessions[1:6]:
            print(f"  {session.name}")
        if len(sessions) > 6:
            print(f"  ... and {len(sessions) - 6} more")
        print("\nAnalyze a specific session with:")
        print("  python scripts/analyze_logs.py <session_name>")


if __name__ == "__main__":
    main()
