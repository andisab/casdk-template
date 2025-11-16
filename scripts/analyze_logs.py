#!/usr/bin/env python3
"""Analyze tool call logs from research agent sessions."""

import json
import sys
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime


def analyze_session(session_dir: Path) -> dict:
    """Analyze a single session's tool call logs."""
    tool_log = session_dir / "tool_calls.jsonl"

    if not tool_log.exists():
        return None

    # Read all tool calls
    tool_calls = []
    with open(tool_log, 'r') as f:
        for line in f:
            try:
                tool_calls.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    if not tool_calls:
        return None

    # Extract stats
    agents = set()
    tools_by_agent = defaultdict(list)
    tool_counts = Counter()
    errors = []

    for call in tool_calls:
        if call['event'] == 'tool_call_start':
            agent_id = call.get('agent_id', 'UNKNOWN')
            tool_name = call.get('tool_name', 'UNKNOWN')

            agents.add(agent_id)
            tools_by_agent[agent_id].append(tool_name)
            tool_counts[tool_name] += 1

        elif call['event'] == 'tool_call_complete':
            if not call.get('success', True):
                errors.append({
                    'agent': call.get('agent_id'),
                    'tool': call.get('tool_name'),
                    'error': call.get('error')
                })

    # Get session timestamp
    session_name = session_dir.name
    timestamp_str = session_name.replace('session_', '')

    try:
        session_time = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
        session_time_formatted = session_time.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        session_time_formatted = timestamp_str

    return {
        'session_dir': session_dir,
        'session_time': session_time_formatted,
        'agents': sorted(agents),
        'tools_by_agent': dict(tools_by_agent),
        'tool_counts': dict(tool_counts),
        'total_calls': len([c for c in tool_calls if c['event'] == 'tool_call_start']),
        'errors': errors
    }


def print_session_summary(stats: dict):
    """Print a summary of session statistics."""
    print(f"\n{'='*70}")
    print(f"Session: {stats['session_dir'].name}")
    print(f"Time: {stats['session_time']}")
    print(f"{'='*70}\n")

    print(f"Agents: {', '.join(stats['agents'])}")
    print(f"Total tool calls: {stats['total_calls']}\n")

    print("Tool Usage:")
    for tool, count in sorted(stats['tool_counts'].items(), key=lambda x: -x[1]):
        print(f"  {tool:20s} {count:3d} calls")

    if stats['errors']:
        print(f"\n⚠️  Errors: {len(stats['errors'])}")
        for err in stats['errors'][:5]:  # Show first 5
            print(f"  - [{err['agent']}] {err['tool']}: {err['error']}")

    print("\nTool Calls by Agent:")
    for agent, tools in sorted(stats['tools_by_agent'].items()):
        tool_summary = Counter(tools)
        print(f"\n  {agent}:")
        for tool, count in sorted(tool_summary.items(), key=lambda x: -x[1]):
            print(f"    {tool:18s} {count:3d}x")


def main():
    """Main entry point."""
    logs_dir = Path("logs")

    if not logs_dir.exists():
        print("No logs directory found.")
        return

    # Find all session directories
    sessions = sorted(
        [d for d in logs_dir.iterdir() if d.is_dir() and d.name.startswith('session_')],
        key=lambda x: x.name,
        reverse=True
    )

    if not sessions:
        print("No session logs found.")
        return

    # If argument provided, analyze specific session
    if len(sys.argv) > 1:
        session_name = sys.argv[1]
        session_path = logs_dir / session_name if '/' not in session_name else Path(session_name)

        if not session_path.exists():
            print(f"Error: Session not found: {session_path}")
            return

        stats = analyze_session(session_path)
        if stats:
            print_session_summary(stats)
        else:
            print(f"No tool call data found in {session_path}")
        return

    # Otherwise, show recent sessions
    print("\n=== Research Agent Log Analysis ===\n")
    print(f"Found {len(sessions)} session(s)\n")

    # Analyze most recent session by default
    recent_session = sessions[0]
    print(f"Analyzing most recent session: {recent_session.name}")

    stats = analyze_session(recent_session)
    if stats:
        print_session_summary(stats)
    else:
        print("No tool call data found in most recent session.")

    if len(sessions) > 1:
        print(f"\n{'='*70}")
        print(f"\nOther sessions ({len(sessions)-1}):")
        for session in sessions[1:6]:  # Show next 5
            print(f"  {session.name}")

        if len(sessions) > 6:
            print(f"  ... and {len(sessions)-6} more")

        print("\nAnalyze a specific session with:")
        print(f"  python scripts/analyze_logs.py <session_name>")


if __name__ == "__main__":
    main()
