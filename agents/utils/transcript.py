"""Transcript handling for conversation history."""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path


def setup_session() -> tuple[Path, Path]:
    """Setup session directory and transcript file.

    Creates a session folder in logs/ with timestamp, containing both
    transcript and detailed tool call logs.

    Returns:
        Tuple of (transcript_file_path, session_dir_path)
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_dir = Path("logs") / f"session_{timestamp}"
    session_dir.mkdir(parents=True, exist_ok=True)

    transcript_file = session_dir / "transcript.txt"

    # Suppress noisy HTTP debug logs from urllib3
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)

    return transcript_file, session_dir


class TranscriptWriter:
    """Helper to write output to both console and transcript file.

    Also owns a small piece of inter-message formatting state: when an
    `AssistantMessage` contains a `ToolUseBlock`, the next text block in a
    later message should start on a new line. Callers signal this with
    ``mark_tool_used()`` and the writer flushes the deferred newline on the
    next ``flush_pending_break()`` (or any text ``write()``).
    """

    def __init__(self, transcript_file: Path):
        # Held open for the writer's lifetime; close()/__exit__ release it.
        self.file = open(transcript_file, "w", encoding="utf-8")  # noqa: SIM115
        self._pending_tool_break = False

    def write(self, text: str, end: str = "", flush: bool = True) -> None:
        """Write text to both console and transcript.

        Note: this does not auto-flush the pending tool break — only
        ``flush_pending_break()`` consumes the flag. Callers writing plain
        text after a tool indicator should call ``flush_pending_break()``
        first.
        """
        print(text, end=end, flush=flush)
        self.file.write(text + end)
        if flush:
            self.file.flush()

    def write_to_file(self, text: str, flush: bool = True) -> None:
        """Write text to transcript file only (not console)."""
        self.file.write(text)
        if flush:
            self.file.flush()

    def mark_tool_used(self) -> None:
        """Note that a tool was just emitted; flush a separating newline next."""
        self._pending_tool_break = True

    def flush_pending_break(self) -> None:
        """If a tool break is pending, emit a newline to separate it from text."""
        if self._pending_tool_break:
            self._pending_tool_break = False
            print(flush=True)
            self.file.write("\n")
            self.file.flush()

    def close(self) -> None:
        """Close the transcript file."""
        self.file.close()

    def __enter__(self) -> TranscriptWriter:
        return self

    def __exit__(self, *_args: object) -> bool:
        self.close()
        return False
