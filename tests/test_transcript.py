"""Tests for agents.utils.transcript."""

from agents.utils.transcript import TranscriptWriter, setup_session


def test_setup_session_creates_logs_dir_and_returns_paths(tmp_cwd):
    transcript_file, session_dir = setup_session()

    assert session_dir.is_dir()
    assert session_dir.parent.name == "logs"
    assert session_dir.name.startswith("session_")
    assert transcript_file.parent == session_dir
    assert transcript_file.name == "transcript.txt"


def test_setup_session_is_idempotent_within_same_second(tmp_cwd):
    setup_session()
    setup_session()


def test_transcript_writer_writes_to_file_and_stdout(transcript_file, capsys):
    writer = TranscriptWriter(transcript_file)
    try:
        writer.write("hello", end="\n")
    finally:
        writer.close()

    assert transcript_file.read_text(encoding="utf-8") == "hello\n"
    assert capsys.readouterr().out == "hello\n"


def test_transcript_writer_write_to_file_skips_stdout(transcript_file, capsys):
    writer = TranscriptWriter(transcript_file)
    try:
        writer.write_to_file("internal\n")
    finally:
        writer.close()

    assert transcript_file.read_text(encoding="utf-8") == "internal\n"
    assert capsys.readouterr().out == ""


def test_transcript_writer_context_manager_closes_file(transcript_file):
    with TranscriptWriter(transcript_file) as writer:
        writer.write("inside", end="")

    assert writer.file.closed
    assert transcript_file.read_text(encoding="utf-8") == "inside"
