# Research Agent - Claude Context

## Project Status

**Current Version**: 0.1.0 (Standalone)
**Status**: Active Development — basic learning harness for the Claude Agent SDK
**SDK floor**: `claude-agent-sdk>=0.1.51` (latest at last refresh: 0.1.68)

> ⚠️ Not sandboxed, not containerized, no monitoring. `permission_mode="bypassPermissions"`
> is the default. See README "Scope & safety" callout before changing.

### Recent Changes
- Modernized for current Claude Agent SDK: `Task` → `Agent` tool rename (allow both for compat)
- Hook callbacks return `{}` (canonical) instead of `{'continue_': True}`
- Removed ~50 LOC of CLI auto-discovery; SDK locates the CLI on `$PATH`
- Switched to `isinstance` checks against SDK-imported `AssistantMessage`/`TextBlock`/`ToolUseBlock`
- Extracted `build_agents()` and `build_options()` factories from `chat()` for testability
- Added `tests/` directory with 40 pytest tests; added `scripts/test.sh`
- Bundled `joplin-research` + `joplin-formatting` skills under `.claude/skills/`
- `report-writer` `AgentDefinition` declares `skills=["joplin-research", "joplin-formatting"]`
  (subagents do **not** inherit project skills)

## Quick Reference

### File Structure
```bash
tree -L 3 -I '__pycache__|*.pyc|.venv|uv.lock|node_modules'
# or
eza -TL 3 --icons --git-ignore
```

### Common Commands

```bash
# Setup
./scripts/setup.sh

# Run agent
./scripts/run.sh
uv run agents/agent.py

# Tests (40 tests, ~0.03s)
./scripts/test.sh
./scripts/test.sh -k message_handler -vv
uv run --group dev pytest

# Logs
python scripts/analyze_logs.py              # Analyze latest session
python scripts/analyze_logs.py session_*    # Analyze specific session
./scripts/clean_logs.sh                     # Clean old logs (keeps 7 days)
./scripts/clean_logs.sh 30                  # Keep 30 days

# Dependencies
uv sync                                     # Install/update
uv sync --group dev                         # Include dev deps (pytest)
uv add <package>                            # Add new dep
```

## Architecture Overview

### Agent Coordination Flow

1. **User Request** → Lead Agent
2. **Lead Agent** analyzes and breaks request into 2–4 subtopics
3. **Lead Agent** spawns 2–4 Researcher subagents in PARALLEL via the `Agent` tool
4. **Researchers** use WebSearch (3–7 searches each) and Write to `workspace/research-notes/`
5. **Lead Agent** waits for all researchers to complete
6. **Lead Agent** spawns Report-Writer subagent via the `Agent` tool
7. **Report-Writer** uses Glob/Read to load research, optionally loads `joplin-research` /
   `joplin-formatting` skills, Write to create report in `workspace/results/`
8. **Lead Agent** confirms completion to user

> **Tool name compatibility**: `Task` → `Agent` rename happened in Claude Code v2.1.63.
> The repo allows BOTH names in `allowed_tools` and matches both in
> `message_handler.SUBAGENT_SPAWN_TOOLS`.

### Hook System

**Purpose**: Track all tool calls across main agent and subagents.

**Implementation**:
- `PreToolUse` hook: captures tool calls before execution
- `PostToolUse` hook: captures results after execution
- Both hooks return `{}` (canonical SDK shape — non-blocking, no decision)
- Uses `parent_tool_use_id` from `AssistantMessage` to attribute calls to the spawning subagent
- Generates unique agent IDs: `RESEARCHER-1`, `RESEARCHER-2`, `REPORT-WRITER-1`, …
- Skips main-agent `Agent`/`Task` calls (those are logged via `register_subagent_spawn`
  from the message stream, not the hook)

**Logging**:
- Console: brief `[AGENT-ID] → ToolName` notifications
- `logs/session_*/transcript.txt`: human-readable full conversation
- `logs/session_*/tool_calls.jsonl`: structured JSON, one event per line

## Configuration

### Agent Definitions

**Built by**: `build_agents(*, researcher_prompt, report_writer_prompt)` in `agents/agent.py`.
Exposed as a module-level factory so tests can construct `AgentDefinition`s without
spinning up a `ClaudeSDKClient`.

Current subagents:
- `researcher`: `tools=["WebSearch", "Write"]`, model `haiku`
- `report-writer`: `tools=["Skill", "Write", "Glob", "Read"]`, model `haiku`,
  `skills=["joplin-research", "joplin-formatting"]`

### SDK Options

**Built by**: `build_options(*, system_prompt, agents, hooks=None)` in `agents/agent.py`.
Returns `ClaudeAgentOptions` with:
- `permission_mode="bypassPermissions"` (default; **change with intent** — anchors README warning)
- `setting_sources=["project"]` (loads project CLAUDE.md, settings, but **not** subagent skills — those go on `AgentDefinition.skills`)
- `allowed_tools=["Agent", "Task"]` (both names for cross-version compat)
- `model="haiku"`
- `cli_path=None` (SDK locates CLI on `$PATH`)

### System Prompts

**Location**: `agents/prompts/`
- `lead_agent.txt`: coordinator behavior; ONLY uses the `Agent` tool (legacy `Task` accepted)
- `researcher.txt`: research gathering; MUST use WebSearch; max 3–4 paragraphs
- `report_writer.txt`: report synthesis; reads from `workspace/research-notes/`, uses skills

### Skills

**Location**: `.claude/skills/`

Bundled:
- `joplin-research/`: research-content templates and citation standards. Routes by request
  type; delegates markdown formatting to `joplin-formatting`.
- `joplin-formatting/`: Joplin-compatible markdown formatting rules.

**Critical**: subagents do not inherit project skills automatically. Each subagent that
needs a skill must list it in `AgentDefinition.skills`.

See `.claude/skills/README.md` for documentation on creating new skills.

## Development Notes

### Adding New Subagent Types

1. Create prompt file: `agents/prompts/your_agent.txt`
2. Add to `build_agents()` in `agents/agent.py`:
   ```python
   "your-agent": AgentDefinition(
       description="Clear description of when to use this agent",
       tools=["Tool1", "Tool2"],
       prompt=load_prompt("your_agent.txt"),
       model="haiku",        # or "sonnet", "opus", "inherit"
       skills=["your-skill"],  # optional; required if subagent uses Skill tool
       maxTurns=10,            # optional; SDK >= 0.1.51, prevents runaway loops
   )
   ```
3. Update `lead_agent.txt` to reference the new agent type
4. Add a regression test in `tests/test_agent_setup.py` asserting on the new entry

> Subagents cannot spawn subagents. Don't include `Agent` or `Task` in their `tools` list.

### Adding New Tools to Existing Agents

Edit the `tools` list in the `AgentDefinition` inside `build_agents()`:
```python
tools=["WebSearch", "Write", "Read", "Edit", "Bash"]
```

**Common tools**: Read, Write, Edit, MultiEdit, Glob, Grep, WebSearch, WebFetch, Bash,
Skill, NotebookEdit, TodoWrite. The subagent-spawn tool is `Agent` (legacy `Task`).

### Modifying Agent Behavior

**Model Selection** (cheap → capable):
- `haiku`: fast, cost-effective (current default)
- `sonnet`: better reasoning
- `opus`: highest capability
- `inherit`: use the parent's model

**Permission Mode** (valid SDK literals):
- `default`: prompt the user for each tool
- `acceptEdits`: auto-approve file edits only
- `plan`: planning-mode (no execution)
- `bypassPermissions`: auto-approve all tools (current default — risky)
- `dontAsk`: skip prompts but enforce the configured policy
- `auto`: SDK-managed

**Working Directory**:
- Files created relative to where the agent is run
- Defaults: `workspace/research-notes/` and `workspace/results/`

## Implementation Details

### Key Files

#### `agents/agent.py`
Entry point. Key symbols:
- `load_prompt(filename)`: load a prompt file from `agents/prompts/`
- `build_agents(*, researcher_prompt, report_writer_prompt)`: factory → `dict[str, AgentDefinition]`
- `build_options(*, system_prompt, agents, hooks=None)`: factory → `ClaudeAgentOptions`
- `chat()`: async REPL using `ClaudeSDKClient`, wires up tracker + hooks + factories

#### `agents/utils/subagent_tracker.py`
Hook implementation. Key features:
- `register_subagent_spawn()`: creates unique agent IDs (called from message stream, not hook)
- `pre_tool_use_hook()`: captures tool calls before execution; returns `{}`
- `post_tool_use_hook()`: captures results after execution; returns `{}`
- `_log_tool_use()`: formats output for console + transcript + JSONL

#### `agents/utils/message_handler.py`
Streams `AssistantMessage` content. Key features:
- `SUBAGENT_SPAWN_TOOLS = ("Agent", "Task")` constant
- Uses `isinstance(block, TextBlock | ToolUseBlock)` for dispatch
- Extracts `parent_tool_use_id` and updates tracker context
- Detects subagent spawns and registers them with the tracker

#### `agents/utils/transcript.py`
Session logging. Key symbols:
- `setup_session()`: creates `logs/session_YYYYMMDD_HHMMSS/`
- `TranscriptWriter`: dual stdout + file writer, supports context manager

### Tests

**Location**: `tests/` (40 tests, ~0.03s)
- `test_agent_setup.py`: behavioral tests for `build_agents()` and `build_options()`
- `test_message_handler.py`: block dispatch, `Agent`/`Task` spawn detection
- `test_subagent_tracker.py`: hook callbacks, JSONL output, attribution
- `test_transcript.py`: session dir, dual writer

**Config**: `[tool.pytest.ini_options]` in `pyproject.toml`, `asyncio_mode = "auto"`.

**Dev deps**: declared in `[dependency-groups] dev` (PEP 735) — `pytest`, `pytest-asyncio`.

## Maintenance Notes

### Log Management

**Session Logs**: auto-created in `logs/session_YYYYMMDD_HHMMSS/`
- Use `clean_logs.sh` to remove old sessions
- `.gitignore` excludes all log contents

**Workspace files**: `workspace/research-notes/` (raw findings), `workspace/results/` (final reports).
`.gitignore` excludes contents but tracks the directory structure.

### Updating Prompts

When modifying `agents/prompts/*.txt`:
1. Make changes
2. Test with a simple query
3. Inspect `logs/session_*/transcript.txt` and `tool_calls.jsonl`
4. Run `./scripts/test.sh` to confirm nothing structural broke

**Common prompt issues**:
- Researchers not using WebSearch → strengthen "MANDATORY" language
- Reports too long → adjust word-count limits in `report_writer.txt`
- Lead agent doing research itself → emphasize delegation-only role

### Dependency Updates

```bash
uv sync --upgrade                   # Upgrade everything within constraints
uv add --upgrade claude-agent-sdk   # Bump a single package
```

When bumping `claude-agent-sdk`, re-check the [subagents docs](https://code.claude.com/docs/en/agent-sdk/subagents)
for new `AgentDefinition` fields and run `./scripts/test.sh`.

## Known Issues / Gotchas

1. **Subagents do not inherit project skills.** Even with `setting_sources=["project"]`,
   each subagent that uses the `Skill` tool must list its skills explicitly in
   `AgentDefinition.skills`. The `joplin-research` → `joplin-formatting` chain requires
   BOTH names on the report-writer.
2. **Researchers must use WebSearch.** Prompts emphasize this but Claude may rely on
   training knowledge. Monitor and tighten prompts if needed.
3. **Parallel spawning.** Lead agent should spawn all researchers at once; the prompt
   emphasizes this but may need reinforcement.
4. **File paths.** All file operations are relative to the working directory. Run from
   project root.
5. **Hook timing.** `parent_tool_use_id` is on messages from inside subagents, not on
   the main agent's messages.
6. **Tool-name dual support.** `block.name` may be `"Agent"` (current) or `"Task"`
   (pre-v2.1.63). Always match both. The constant `SUBAGENT_SPAWN_TOOLS` centralizes this.

## Future Enhancements

### Potential Subagents
- [ ] Fact-checking subagent
- [ ] Data-analysis subagent (Python/Pandas)
- [ ] Citation-validation subagent
- [ ] Multi-report summary subagent
- [ ] Visualization subagent (charts/graphs)

### Tooling
- [ ] Cost tracking (token usage per agent)
- [ ] Retry logic for failed tool calls
- [ ] Filesystem subagent loading (`.claude/agents/*.md`) alongside programmatic ones
- [ ] Web UI for session management
- [ ] Export formats (PDF, Markdown, JSON)

### Possible MCP Servers
- **Joplin MCP**: persistent note storage
- **Memory MCP**: cross-session knowledge
- **Browser MCP**: interactive web research

## Troubleshooting

### Common Errors

**`ANTHROPIC_API_KEY not found`**
- Run `./scripts/setup.sh`
- Verify `.env` exists with a valid key

**`uv: command not found`**
- Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Restart shell

**`claude` CLI not found**
- The SDK requires the Claude Code CLI on `$PATH`
- Install: `npm install -g @anthropic-ai/claude-code`
- Verify: `which claude`

**`No module named 'agents'`**
- Run `uv sync` to install the project
- Run from project root

**Empty reports or missing files**
- Check `logs/session_*/transcript.txt` for errors
- Run `python scripts/analyze_logs.py` for tool-call summary
- Verify researchers used WebSearch (transcript will show)

### Debug Mode

For verbose output:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## See Also

- **README.md**: user-facing documentation (with prominent safety/scope callout)
- **.claude/skills/README.md**: skills documentation and examples
- **pyproject.toml**: dependency configuration + pytest config + dev group
- **tests/**: behavioral test suite
