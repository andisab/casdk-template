# Sample Agentic Team: Multi-Agent Research System

[![CI](https://github.com/andisab/casdk-template/actions/workflows/ci.yml/badge.svg)](https://github.com/andisab/casdk-template/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A standalone multi-agent research system built on the [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/python). A lead agent decomposes a topic into subtopics, dispatches researcher subagents in parallel, and then synthesizes their findings via a report-writer subagent.

> ⚠️ **Scope & safety — please read before running**
>
> This project is a **basic learning harness for the Claude Agent SDK**, intended for experimentation and for understanding the fundamentals of subagents, hooks, skills, and session tracking. **It is not production-ready.** In particular:
>
> - **Not sandboxed, not containerized.** Agents run with your shell user's permissions and write directly to your filesystem. 
> - **No special safeguards against prompt injection,** so be selective and thoughtful about what sites you are searching with the harness in present state. 
> - **`permission_mode="bypassPermissions"` is the default**, which auto-approves every tool call (web searches, file writes, etc.). Fine for local exploration on trusted directories; inadvisable elsewhere.
> - **No monitoring, metrics, or alerting.** Logs are plain files under `logs/`. There is no cost tracking, rate limiting, dashboard, or telemetry export.
> - **No retry or failure-recovery logic** beyond what the SDK itself provides.
> - **Single user, single session.** No multi-tenant safeguards, no authentication, no queueing.
> - **No secret management** beyond reading `ANTHROPIC_API_KEY` from a local `.env`.
>
> Use it to learn the SDK, fork it, and add the hardening your environment needs. For more featureful or differently-shaped starting points, see Anthropic's official reference implementations — [`anthropics/claude-agent-sdk-demos`](https://github.com/anthropics/claude-agent-sdk-demos) (the demos repo this template was originally extracted from), [`anthropics/claude-quickstarts`](https://github.com/anthropics/claude-quickstarts) (customer-support agent, financial-data-analyst, computer-use, etc.), and [`anthropics/claude-cookbooks`](https://github.com/anthropics/claude-cookbooks) (recipes for tool use, RAG, multimodal, etc.). If you specifically want a Docker-based harness with sandboxing and observability layered on top of the SDK, see the companion [`casdk-harness`](https://github.com/andisab/casdk-harness) project.

## Features

- **Multi-agent coordination** — Lead agent orchestrates researcher and report-writer subagents
- **Parallel execution** — Multiple researchers investigate distinct subtopics simultaneously
- **Hook-based tracking** — `PreToolUse` / `PostToolUse` hooks capture every tool call and attribute it to the right subagent via `parent_tool_use_id`
- **Skills** — Subagents can opt into project-local skills (the bundled `joplin-research` + `joplin-formatting` pair is a worked example of a routing skill that delegates to a formatting skill)
- **Structured logs** — Per-session transcripts (`transcript.txt`) plus JSONL tool-call records (`tool_calls.jsonl`)
- **Test suite** — pytest-based unit and smoke tests in `tests/`

## Quick Start

> 💡 **Starting a new project?** Click **Use this template** on GitHub to fork without inheriting history, or `gh repo create my-project --template andisab/casdk-template`.

### Prerequisites

- Python ≥ 3.10
- [uv](https://github.com/astral-sh/uv) package manager
- Claude Code CLI on `$PATH` — install with `npm install -g @anthropic-ai/claude-code` if missing
- Anthropic API key ([get one here](https://console.anthropic.com/settings/keys))

### Installation

1. Run the setup script:
   ```bash
   ./scripts/setup.sh
   ```

2. Add your API key to `.env`:
   ```bash
   ANTHROPIC_API_KEY=your_api_key_here
   ```

3. Run the agent:
   ```bash
   ./scripts/run.sh
   # or
   uv run agents/agent.py
   ```

### Example Usage

```
You: Research recent developments in quantum computing

Agent: Researching 4 areas: hardware/qubits, algorithms/applications,
       industry players/investments, and challenges/timeline.
       Spawning researchers.

[🚀 Spawning RESEARCHER-1: Quantum hardware and qubit technology]
[🚀 Spawning RESEARCHER-2: Quantum algorithms and applications]
[🚀 Spawning RESEARCHER-3: Industry players and investments]
[🚀 Spawning RESEARCHER-4: Challenges and timeline]

[Researchers complete their work...]

[🚀 Spawning REPORT-WRITER-1: Synthesize research into final report]

Agent: Complete. Report: workspace/results/quantum_computing_summary_YYYYMMDD.txt
```

## Architecture

### Agent Hierarchy

```
┌─────────────────┐
│   Lead Agent    │  Coordinator (uses only the Agent tool)
└────────┬────────┘
         │
         ├─────────────────────┬─────────────────────┬─────────────────────┐
         │                     │                     │                     │
    ┌────▼──────┐       ┌──────▼──────┐      ┌──────▼──────┐      ┌──────▼──────┐
    │RESEARCHER-1│       │RESEARCHER-2 │      │RESEARCHER-3 │      │RESEARCHER-4 │
    │ Subtopic A │       │ Subtopic B  │      │ Subtopic C  │      │ Subtopic D  │
    └────┬───────┘       └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
         │                      │                     │                     │
         │ WebSearch, Write     │ WebSearch, Write    │ WebSearch, Write    │ WebSearch, Write
         │                      │                     │                     │
         └──────────────────────┴─────────────────────┴─────────────────────┘
                                         │
                                    ┌────▼────────────┐
                                    │ REPORT-WRITER-1 │
                                    │ Reads, synthesizes,│
                                    │ creates report  │
                                    └─────────────────┘
                                    Glob, Read, Write, Skill
```

### Agent Types

#### Lead Agent
- **Role**: Orchestrates the entire research process
- **Tools**: `Agent` (only) — the subagent-spawning tool. Named `Task` on Claude Code builds before v2.1.63; the project allows both names for compatibility.
- **Model**: Haiku
- **Responsibilities**:
  - Breaks research requests into 2–4 subtopics
  - Spawns researcher subagents in parallel
  - Waits for all research to complete
  - Spawns report-writer to synthesize findings

#### Researcher Subagents
- **Role**: Gathers information on specific subtopics
- **Tools**: `WebSearch`, `Write`
- **Model**: Haiku
- **Responsibilities**:
  - Conducts 3–7 web searches per subtopic
  - Extracts key findings from authoritative sources
  - Saves concise research notes to `workspace/research-notes/`

#### Report-Writer Subagent
- **Role**: Synthesizes research into professional reports
- **Tools**: `Glob`, `Read`, `Write`, `Skill`
- **Skills**: `joplin-research` + `joplin-formatting` (both declared on the `AgentDefinition`; subagents do not inherit project skills automatically, and `joplin-research` delegates markdown formatting to `joplin-formatting`, so both must be reachable)
- **Model**: Haiku
- **Responsibilities**:
  - Reads all research notes from `workspace/research-notes/`
  - Applies formatting guidelines from the loaded skill
  - Creates the final report in `workspace/results/`

### About the Joplin output format

[Joplin](https://joplinapp.org) is a free, open-source, cross-platform note-taking app (desktop on Windows / macOS / Linux, mobile on iOS / Android, plus a terminal client). It stores notes as Markdown with optional end-to-end-encrypted sync over WebDAV, Nextcloud, Dropbox, OneDrive, S3, or Joplin Cloud. Source and downloads: <https://github.com/laurent22/joplin>.

The bundled `joplin-research` and `joplin-formatting` skills produce reports tuned for Joplin's renderer — heading hierarchy, link styling, callouts, code blocks, and tables follow the conventions Joplin's CSS expects. The output is plain Markdown, so it also renders fine in any other Markdown viewer; the formatting is just *optimized* for Joplin. To use a generated report, copy the contents of `workspace/results/<report>.md` into a new Joplin note (or use the Joplin import feature for a `.md` file).

> The Joplin skills are an example of a "routing skill that delegates to a formatting skill." If you don't use Joplin, you can swap in your own formatting skill (e.g. for Notion, Obsidian, Confluence) following the same pattern — see `.claude/skills/README.md`.

## Project Structure

```
casdk-template/
├── .env.example                 # Environment variables template
├── .gitignore
├── pyproject.toml               # Project + dev dependency groups + pytest config
├── README.md                    # This file
├── CLAUDE.md                    # Project context for Claude Code
│
├── agents/                      # Application package
│   ├── agent.py                 # Entry point (ClaudeSDKClient + AgentDefinitions + hooks)
│   ├── prompts/                 # Agent system prompts
│   │   ├── lead_agent.txt
│   │   ├── researcher.txt
│   │   └── report_writer.txt
│   └── utils/
│       ├── message_handler.py   # Block dispatch, subagent spawn detection
│       ├── subagent_tracker.py  # Hook callbacks, JSONL log, parent_tool_use_id attribution
│       └── transcript.py        # Session directory + dual stdout/file writer
│
├── .claude/                     # Claude Code project settings
│   └── skills/
│       ├── README.md            # Skills documentation
│       ├── joplin-research/     # Bundled skill: Joplin-formatted research output
│       │   ├── SKILL.md         # Routes by request type (rundown, survey, summary, ...)
│       │   └── resources/
│       │       ├── citation-guide.md
│       │       ├── image-policy.md
│       │       └── templates/   # article-summary, book-summary, research-notes,
│       │                        # technical-rundown, technical-survey, whitepaper-summary
│       └── joplin-formatting/   # Markdown formatting rules; invoked by joplin-research
│           ├── SKILL.md
│           └── resources/
│               ├── css-reference.md
│               ├── element-catalog.md
│               └── validate_joplin_md.py
│
├── scripts/                     # Development utilities
│   ├── setup.sh                 # Initial setup (uv sync, .env scaffolding)
│   ├── run.sh                   # Quick run wrapper
│   ├── test.sh                  # Run the test suite (forwards args to pytest)
│   ├── clean_logs.sh            # Clean old session logs
│   └── analyze_logs.py          # Parse session JSONL logs
│
├── tests/                       # Unit + smoke tests
│   ├── conftest.py              # Shared fixtures
│   ├── test_agent_setup.py      # Module-import smoke + regression guards
│   ├── test_message_handler.py  # Block dispatch, Agent / Task spawn detection
│   ├── test_subagent_tracker.py # Hook returns, JSONL output, attribution
│   └── test_transcript.py       # setup_session, TranscriptWriter
│
├── workspace/                   # Generated by agents (gitignored)
│   ├── research-notes/
│   └── results/
│
└── logs/                        # Session logs (gitignored)
    └── session_YYYYMMDD_HHMMSS/
        ├── transcript.txt       # Human-readable log
        └── tool_calls.jsonl     # Structured tool data
```

## Development

### Adding New Subagent Types

1. Create a new prompt file in `agents/prompts/`.
2. Define the agent in `agents/agent.py`:

   ```python
   agents = {
       "your-agent": AgentDefinition(
           description="What this agent does and when to use it",
           tools=["Tool1", "Tool2"],
           prompt=load_prompt("your_agent.txt"),
           model="haiku",
           # Optional: declare project skills the subagent can load
           skills=["your-skill"],
           # Optional: cap turns to prevent runaway loops
           maxTurns=10,
       )
   }
   ```

3. Update the lead agent prompt to know when to use the new agent.

> Subagents cannot spawn their own subagents. Don't include `Agent` in a subagent's `tools` list.

### Adding New Tools

To give an agent additional tools, edit its `tools` list in the `AgentDefinition`:

```python
tools=["WebSearch", "Write", "Bash", "Read"]
```

Common tools: `WebSearch`, `WebFetch`, `Write`, `Read`, `Edit`, `Glob`, `Grep`, `Bash`, `Agent`, `Skill`. See the [SDK docs](https://code.claude.com/docs/en/agent-sdk/python) for the full list.

### Creating Custom Skills

Skills are optional, modular knowledge packages that agents can load on demand. To create one:

```bash
mkdir -p .claude/skills/your-skill-name
# Create SKILL.md (and an optional resources/ subdir)
```

Then declare the skill on each subagent that should be able to load it:

```python
AgentDefinition(
    ...,
    skills=["your-skill-name"],
)
```

> ⚠️ Subagents do **not** inherit project skills automatically — even with `setting_sources=["project"]`. Each subagent that needs a skill must list it explicitly. See `.claude/skills/README.md` for detailed examples and the bundled `joplin-research` skill for a working reference.

### Analyzing Sessions

```bash
# Most recent session
python scripts/analyze_logs.py

# A specific session
python scripts/analyze_logs.py session_YYYYMMDD_HHMMSS
```

### Running Tests

The test suite covers the utility modules, hook callbacks, and key SDK regressions (e.g. the `Task` → `Agent` tool rename, canonical hook return shape, and the `skills=[…]` declaration on the report-writer).

```bash
# Run the full suite
./scripts/test.sh

# Or directly via uv (installs dev deps on first run)
uv run --group dev pytest

# Filter by name
./scripts/test.sh -k message_handler -vv
```

### Linting

Style and import order are enforced with [ruff](https://docs.astral.sh/ruff/). CI runs `ruff check` and `ruff format --check` on every push.

```bash
# Check
./scripts/lint.sh

# Auto-fix what can be fixed
uv run --group dev ruff check --fix
uv run --group dev ruff format
```

### Cleaning Logs

```bash
# Keep last 7 days (default)
./scripts/clean_logs.sh

# Keep last 30 days
./scripts/clean_logs.sh 30
```

## How It Works

### Subagent Tracking with Hooks

The system registers `PreToolUse` and `PostToolUse` hooks that fire for every tool call, regardless of which agent issues it:

```python
hooks = {
    "PreToolUse":  [HookMatcher(matcher=None, hooks=[tracker.pre_tool_use_hook])],
    "PostToolUse": [HookMatcher(matcher=None, hooks=[tracker.post_tool_use_hook])],
}
```

**Key features:**
- Tracks which agent (`RESEARCHER-1`, `RESEARCHER-2`, `REPORT-WRITER-1`, …) issued which tool calls.
- Logs input parameters and outputs.
- Associates each call with the parent Agent invocation via `parent_tool_use_id`.
- Writes both human-readable transcripts and structured JSONL records.
- Hooks return `{}` (canonical SDK shape — non-blocking, no decision).

### Message Flow

1. User sends a research request.
2. Lead agent analyzes it and breaks it into subtopics.
3. Lead agent spawns researchers in parallel using the `Agent` tool.
4. Each researcher runs in its own context; messages from inside that subagent carry a `parent_tool_use_id` linking back to the spawning tool call. Hooks use that ID to attribute every nested tool call to the correct researcher.
5. Researchers complete and save findings to `workspace/research-notes/`.
6. Lead agent spawns the report-writer.
7. Report-writer reads the notes, optionally loads the `joplin-research` skill, and writes the final report to `workspace/results/`.

## Configuration

### Environment Variables

- `ANTHROPIC_API_KEY` — Anthropic API key (required)

### Customization Options

Subagent definitions and SDK options are constructed by two factory functions in `agents/agent.py`:

- **`build_agents(*, researcher_prompt, report_writer_prompt)`** — returns the `dict[str, AgentDefinition]` of subagents. Edit this to change models, tools, skill declarations, or to add new subagents. Calling it from a test (with dummy prompt strings) lets you assert on the constructed `AgentDefinition`s without spinning up a session — see `tests/test_agent_setup.py`.
- **`build_options(*, system_prompt, agents, hooks=None)`** — returns the `ClaudeAgentOptions`. Edit this to change `permission_mode`, `model`, `allowed_tools`, `setting_sources`, or to pass `cwd=...`.

Common knobs:

- **Models**: `model="haiku"` → `"sonnet"` or `"opus"` for stronger reasoning at higher cost. `"inherit"` is also valid on subagents (use the parent's model).
- **Permission mode**: replace `"bypassPermissions"` with one of the documented values: `"default"` (prompt for each tool), `"acceptEdits"`, `"plan"`, `"dontAsk"`, or `"auto"`. See the [SDK docs](https://code.claude.com/docs/en/agent-sdk/python) for the current semantics of each.
- **Allowed tools**: tighten or loosen the per-agent `tools` lists in `build_agents()`.
- **Working directory**: pass `cwd=...` on `ClaudeAgentOptions` to redirect file output.

## Troubleshooting

### `ANTHROPIC_API_KEY not found`

Run `./scripts/setup.sh` and edit `.env` with your API key.

### `Command 'uv' not found`

Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Claude CLI not found

The Claude Agent SDK requires the Claude Code CLI on `$PATH`. Install it:

```bash
npm install -g @anthropic-ai/claude-code
# verify
which claude
```

### No research output

If the agent runs but no files appear in `workspace/`, check:
- File output is relative to the directory where you invoked the agent.
- The `workspace/` directory is created automatically — check write permissions.
- Inspect session logs: `cat logs/session_*/transcript.txt` and `logs/session_*/tool_calls.jsonl`.

## About this repo

This is a personal learning template for the Claude Agent SDK; issues and pull requests are not actively triaged. The expected use pattern is to fork it (or click **Use this template**) and adapt it to your own project. The architecture, prompts, and skills are all intended to be edited.

## Roadmap

- Rate limiting and budget caps on top of the per-session cost reporting
- Optional Agent-as-a-file (`.claude/agents/*.md`) loading alongside programmatic `AgentDefinition`s
- More worked-example skills (citations, structured-output formatting, domain-specific research types)

## Resources

- [Claude Agent SDK – Python](https://code.claude.com/docs/en/agent-sdk/python)
- [Claude Agent SDK – Subagents guide](https://code.claude.com/docs/en/agent-sdk/subagents)
- [Claude API Reference](https://docs.anthropic.com/claude)

## License

Based on the Claude Agent SDK demo by Anthropic. Modified for standalone development.
