# Research Agent - Claude Context

## Project Status

**Current Version**: 0.1.0 (Standalone)
**Status**: Active Development
**Based On**: Claude Agent SDK Research Demo

### Recent Changes
- Extracted from claude-agent-sdk-demos repository
- Added development scripts and tooling
- Created custom skills structure
- Enhanced documentation for standalone use

## Quick Reference

### File Structure
```bash
# View full structure
tree -L 3 -I '__pycache__|*.pyc|.venv|uv.lock'

# Or with eza if available
eza -TL 3 --icons --git-ignore
```

### Common Commands

```bash
# Setup
./scripts/setup.sh

# Run agent
./scripts/run.sh
uv run research_agent/agent.py

# Development
python scripts/analyze_logs.py              # Analyze latest session
python scripts/analyze_logs.py session_*    # Analyze specific session
./scripts/clean_logs.sh                     # Clean old logs (keeps 7 days)
./scripts/clean_logs.sh 30                  # Keep 30 days

# Testing
python test_hooks.py                        # Test hook system

# Dependency management
uv sync                                     # Install/update dependencies
uv add <package>                           # Add new dependency
```

## Architecture Overview

### Agent Coordination Flow

1. **User Request** → Lead Agent
2. **Lead Agent** analyzes and breaks into 2-4 subtopics
3. **Lead Agent** spawns 2-4 Researcher subagents in PARALLEL via Task tool
4. **Researchers** use WebSearch (3-7 searches each) and Write to `c-w-d/research-notes/`
5. **Lead Agent** waits for all researchers to complete
6. **Lead Agent** spawns Report-Writer subagent via Task tool
7. **Report-Writer** uses Glob/Read to load research, Write to create report in `c-w-d/results`
8. **Lead Agent** confirms completion to user

### Hook System

**Purpose**: Track all tool calls across main agent and subagents

**Implementation**:
- `PreToolUse` hook: Captures tool calls before execution
- `PostToolUse` hook: Captures results after execution
- Uses `parent_tool_use_id` to link tool calls to spawning Task
- Generates unique agent IDs (RESEARCHER-1, RESEARCHER-2, etc.)

**Logging**:
- Console: Brief tool use notifications
- `logs/session_*/transcript.txt`: Human-readable full conversation
- `logs/session_*/tool_calls.jsonl`: Structured JSON for analysis

## Configuration

### Agent Definitions

**Location**: `research_agent/agent.py`

Current subagent types:
- `researcher`: WebSearch + Write tools
- `report-writer`: Glob + Read + Write + Skill tools

### System Prompts

**Location**: `research_agent/prompts/`

- `lead_agent.txt`: Coordinator behavior (ONLY uses Task tool)
- `researcher.txt`: Research gathering (MUST use WebSearch, max 3-4 paragraphs)
- `report_writer.txt`: Report synthesis (reads from files/, uses skills)

### Skills

**Location**: `.claude/skills/`

- `professional-research-summary`: Report formatting guidelines
- Add new skills by creating directories with `SKILL.md` files

## Development Notes

### Adding New Subagent Types

1. Create prompt file: `research_agent/prompts/your_agent.txt`
2. Add to `agents` dict in `agent.py`:
```python
"your-agent": AgentDefinition(
    description="Clear description of when to use this agent",
    tools=["Tool1", "Tool2"],
    prompt=load_prompt("your_agent.txt"),
    model="haiku"  # or "sonnet", "opus"
)
```
3. Update `lead_agent.txt` to reference new agent type

### Adding New Tools to Existing Agents

Edit the `tools` list in `AgentDefinition`:
```python
tools=["WebSearch", "Write", "Read", "Edit", "Bash"]
```

**Available Tools**:
- File: Read, Write, Edit, MultiEdit, Glob, NotebookEdit
- Search: Grep, WebSearch, WebFetch
- Execution: Bash, Task
- Utilities: TodoWrite, Skill, BashOutput, KillShell
- Planning: ExitPlanMode

### Modifying Agent Behavior

**Model Selection**:
- `haiku`: Fast, cost-effective (current default)
- `sonnet`: Better reasoning, more expensive
- `opus`: Highest capability, highest cost

**Permission Mode**:
- `bypassPermissions`: Auto-approve all tools (current)
- `permissionRequired`: Manual approval for each tool

**Working Directory**:
- Files created relative to where agent is run
- Default: `files/research_notes/` and `files/reports/`

## Implementation Details

### Key Files

#### `research_agent/agent.py`
Main entry point. Key functions:
- `load_prompt()`: Loads prompts from files
- `chat()`: Main async loop, handles user input
- Sets up hooks, agents, and SDK options

#### `research_agent/utils/subagent_tracker.py`
Hook implementation for tracking. Key features:
- `register_subagent_spawn()`: Creates unique agent IDs
- `pre_tool_use_hook()`: Captures tool calls before execution
- `post_tool_use_hook()`: Captures results after execution
- `_log_tool_use()`: Formats output for console and files

#### `research_agent/utils/message_handler.py`
Processes message stream. Key features:
- Extracts `parent_tool_use_id` from messages
- Detects Task tool usage (subagent spawning)
- Updates tracker context
- Formats console output

#### `research_agent/utils/transcript.py`
Session logging utilities:
- `setup_session()`: Creates timestamped log directory
- `TranscriptWriter`: Dual output (console + file)

## Maintenance Notes

### Log Management

**Session Logs**: Automatically created in `logs/session_YYYYMMDD_HHMMSS/`
- Keep or archive important sessions
- Use `clean_logs.sh` to remove old sessions
- Default .gitignore excludes all log contents

**Research Files**: Created in `files/`
- `c-w-d/research-notes/`: Raw research from researchers
- `c-w-d/results/`: Final synthesized reports
- .gitignore excludes file contents but tracks directory structure

### Updating Prompts

When modifying prompts, test thoroughly:
1. Make changes to `.txt` files in `research_agent/prompts/`
2. Test with simple query first
3. Check logs for unexpected behavior
4. Verify tool usage is as expected

**Common Prompt Issues**:
- Researchers not using WebSearch → Strengthen "MANDATORY" language
- Reports too long → Adjust word count limits
- Lead agent doing research itself → Emphasize delegation-only role

### Dependency Updates

```bash
# Check for updates
uv pip list --outdated

# Update specific package
uv add --upgrade claude-agent-sdk

# Update all
uv sync --upgrade
```

## Known Issues / Gotchas

1. **Researchers must use WebSearch**: Prompts emphasize this but Claude may sometimes rely on training knowledge. Monitor and adjust prompts if needed.

2. **Parallel spawning**: Lead agent should spawn all researchers at once, not sequentially. Prompts emphasize this but may need reinforcement.

3. **File paths**: All file operations are relative to working directory. Ensure you run from project root.

4. **Hook timing**: `parent_tool_use_id` is only available in messages from subagents, not in the main agent's messages.

## Future Enhancements

### Potential Additions

- [ ] Add fact-checking subagent type
- [ ] Create data analysis subagent (uses Python, Pandas)
- [ ] Add citation validation subagent
- [ ] Create summary subagent (for multi-report synthesis)
- [ ] Add visualization subagent (creates charts, graphs)
- [ ] Implement retry logic for failed tool calls
- [ ] Add cost tracking (token usage per agent)
- [ ] Create web UI for session management
- [ ] Add export formats (PDF, Markdown, JSON)

### Tools to Consider Adding

- **Joplin MCP**: For persistent note storage
- **Memory MCP**: For cross-session knowledge
- **Browser MCP**: For interactive web research
- **Python execution**: For data analysis
- **Image generation**: For visual content

## Troubleshooting

### Common Errors

**"ANTHROPIC_API_KEY not found"**
- Run `./scripts/setup.sh`
- Verify `.env` file exists and has valid key

**"uv: command not found"**
- Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Restart shell after installation

**"No module named 'research_agent'"**
- Run `uv sync` to install dependencies
- Ensure running from project root

**Empty reports or missing files**
- Check session logs: `cat logs/session_*/transcript.txt`
- Verify file paths in tool calls: `python scripts/analyze_logs.py`
- Ensure researchers are using WebSearch (check transcript)

### Debug Mode

For more verbose output, modify `agent.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## See Also

- **README.md**: User-facing documentation
- **test_hooks.py**: Hook system testing
- **.claude/skills/README.md**: Skills documentation
- **pyproject.toml**: Dependency configuration
