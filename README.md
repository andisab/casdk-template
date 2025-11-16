# Multi-Agent Research System

A standalone multi-agent research system built with the Claude Agent SDK. This system coordinates specialized subagents to research any topic and generate comprehensive reports.

## Features

- **Multi-Agent Coordination**: Lead agent orchestrates specialized researcher and report-writer subagents
- **Parallel Research**: Multiple researchers investigate different subtopics simultaneously
- **Comprehensive Tracking**: Detailed logging of all subagent activities via SDK hooks
- **Professional Reports**: Synthesized research findings in structured, citation-rich formats
- **Extensible Architecture**: Easy to add new subagent types, tools, and capabilities

## Quick Start

### Prerequisites

- Python >= 3.10
- [uv](https://github.com/astral-sh/uv) package manager
- Anthropic API key ([get one here](https://console.anthropic.com/settings/keys))

### Installation

1. Clone or navigate to this directory

2. Run the setup script:
```bash
./scripts/setup.sh
```

3. Add your API key to `.env`:
```bash
# Edit .env and replace with your actual key
ANTHROPIC_API_KEY=your_api_key_here
```

4. Run the agent:
```bash
./scripts/run.sh
# or
uv run research_agent/agent.py
```

### Example Usage

**Simple single-line prompt:**
```
You: Research quantum computing developments in 2025

Agent: Researching 4 areas: hardware/qubits, algorithms/applications,
       industry players/investments, and challenges/timeline.
       Spawning researchers.

[🚀 Spawning RESEARCHER-1: Quantum hardware and qubit technology]
[🚀 Spawning RESEARCHER-2: Quantum algorithms and applications]
[🚀 Spawning RESEARCHER-3: Industry players and investments]
[🚀 Spawning RESEARCHER-4: Challenges and timeline]

[Researchers complete their work...]

[🚀 Spawning REPORT-WRITER-1: Synthesize research into final report]

Agent: Complete. Report: files/reports/quantum_computing_summary_20251115.txt
```

**Multi-line prompt with images (Meta+Enter for newlines):**
```
You: Analyze this system architecture diagram: [Meta+Enter]
...  [Meta+Enter]
...  @image:~/Documents/architecture.png
  ✓ Image attached: ~/Documents/architecture.png
...  [Meta+Enter]
...  Identify potential bottlenecks and suggest improvements. [Enter]

Agent: [Analyzes image and provides feedback]
```

**Key Controls:**
- **Meta+Enter (or Esc then Enter)**: New line
- **Enter**: Submit prompt
- **@image:/path**: Attach image

See [MULTILINE_INPUT_GUIDE.md](./MULTILINE_INPUT_GUIDE.md) for complete usage instructions.

## Architecture

### Agent Hierarchy

```
┌─────────────────┐
│   Lead Agent    │  Coordinator (uses only Task tool)
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
                                    │ Reads, Synthesizes,│
                                    │ Creates Report  │
                                    └─────────────────┘
                                    Glob, Read, Write, Skill
```

### Agent Types

#### Lead Agent
- **Role**: Orchestrates the entire research process
- **Tools**: Task (only)
- **Model**: Haiku
- **Responsibilities**:
  - Breaks research requests into 2-4 subtopics
  - Spawns researcher subagents in parallel
  - Waits for all research to complete
  - Spawns report-writer to synthesize findings

#### Researcher Subagents
- **Role**: Gathers information on specific subtopics
- **Tools**: WebSearch, Write
- **Model**: Haiku
- **Responsibilities**:
  - Conducts 3-7 web searches per subtopic
  - Extracts key findings from authoritative sources
  - Saves concise research notes to `files/research_notes/`

#### Report-Writer Subagent
- **Role**: Synthesizes research into professional reports
- **Tools**: Glob, Read, Write, Skill
- **Model**: Haiku
- **Responsibilities**:
  - Reads all research notes from `files/research_notes/`
  - Applies professional formatting guidelines from skills
  - Creates comprehensive reports in `files/reports/`

## Project Structure

```
research/
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore rules
├── pyproject.toml           # Python project configuration
├── test_hooks.py            # Hook testing utility
├── README.md                # This file
├── CLAUDE.md                # Project context for Claude
│
├── research_agent/          # Main package
│   ├── agent.py            # Entry point
│   ├── prompts/            # Agent system prompts
│   │   ├── lead_agent.txt
│   │   ├── researcher.txt
│   │   └── report_writer.txt
│   └── utils/              # Utility modules
│       ├── message_handler.py    # Message processing
│       ├── subagent_tracker.py   # Hook-based tracking
│       └── transcript.py         # Session logging
│
├── .claude/                # Claude Code project settings
│   └── skills/            # Custom skills for agents
│       ├── README.md
│       └── professional-research-summary/
│           └── SKILL.md
│
├── scripts/               # Development utilities
│   ├── setup.sh          # Initial setup
│   ├── run.sh            # Quick run wrapper
│   ├── clean_logs.sh     # Clean old logs
│   └── analyze_logs.py   # Parse session logs
│
├── files/                # Generated by agents (gitignored)
│   ├── research_notes/   # Raw research findings
│   └── reports/          # Final synthesized reports
│
└── logs/                 # Session logs (gitignored)
    └── session_YYYYMMDD_HHMMSS/
        ├── transcript.txt       # Human-readable log
        └── tool_calls.jsonl     # Structured tool data
```

## Development

### Adding New Subagent Types

1. Create a new prompt file in `research_agent/prompts/`
2. Define the agent in `agent.py`:

```python
agents = {
    "your-agent": AgentDefinition(
        description="What this agent does and when to use it",
        tools=["Tool1", "Tool2"],
        prompt=load_prompt("your_agent.txt"),
        model="haiku"
    )
}
```

3. Update the lead agent prompt to know when to use the new agent

### Adding New Tools

To give agents access to additional tools, update the `tools` list in the `AgentDefinition`:

```python
tools=["WebSearch", "Write", "Bash", "Read"]
```

Available tools include: WebSearch, Write, Read, Edit, Glob, Grep, Bash, Task, Skill, and more.

### Creating Custom Skills

Add skills to `.claude/skills/` for specialized formatting or domain knowledge:

```bash
mkdir -p .claude/skills/your-skill-name
# Create SKILL.md with your content
```

Reference in prompts:
```
Load the "your-skill-name" skill for guidelines on [task].
```

### Analyzing Sessions

View detailed tool call statistics:

```bash
# Analyze most recent session
python scripts/analyze_logs.py

# Analyze specific session
python scripts/analyze_logs.py session_20251115_143022
```

### Cleaning Logs

Remove old session logs:

```bash
# Keep last 7 days (default)
./scripts/clean_logs.sh

# Keep last 30 days
./scripts/clean_logs.sh 30
```

## How It Works

### Subagent Tracking with Hooks

The system uses SDK hooks to track every tool call made by any agent:

```python
hooks = {
    'PreToolUse': [HookMatcher(hooks=[tracker.pre_tool_use_hook])],
    'PostToolUse': [HookMatcher(hooks=[tracker.post_tool_use_hook])]
}
```

**Key Features:**
- Tracks which agent (RESEARCHER-1, RESEARCHER-2, etc.) uses which tools
- Logs input parameters and outputs
- Associates tool calls with parent Task via `parent_tool_use_id`
- Writes both human-readable transcripts and structured JSONL logs

### Message Flow

1. User sends research request
2. Lead agent analyzes and breaks into subtopics
3. Lead agent spawns researchers in parallel using Task tool
4. Each researcher:
   - Receives unique `parent_tool_use_id` from Task tool
   - All subsequent messages include this ID
   - Hooks use the ID to attribute tool calls to the correct researcher
5. Researchers complete and save findings
6. Lead agent spawns report-writer
7. Report-writer synthesizes and creates final report

## Configuration

### Environment Variables

- `ANTHROPIC_API_KEY`: Your Anthropic API key (required)

### Customization Options

Edit `research_agent/agent.py` to customize:

- **Models**: Change `model="haiku"` to `"sonnet"` or `"opus"` for better performance
- **Permission Mode**: Use `"permissionRequired"` to manually approve tool calls
- **Allowed Tools**: Restrict or expand available tools per agent
- **Working Directory**: Change where files are created

## Troubleshooting

### API Key Issues

```
Error: ANTHROPIC_API_KEY not found.
```

**Solution**: Run `./scripts/setup.sh` and edit `.env` with your API key.

### Missing Dependencies

```
Command 'uv' not found
```

**Solution**: Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### No Research Output

If agents complete but no files are created, check:
- Files are created relative to the working directory where you run the agent
- The `files/` directory should be created automatically
- Check session logs for errors: `cat logs/session_*/transcript.txt`

## Contributing

This is a standalone project. Feel free to:
- Add new subagent types
- Enhance existing prompts
- Create new skills
- Improve tracking and logging
- Add new development tools

## Resources

- [Claude Agent SDK Documentation](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-overview)
- [Claude API Reference](https://docs.anthropic.com/claude)
- [Example Research Reports](./files/reports/) (after running)

## License

Based on the Claude Agent SDK demo by Anthropic. Modified for standalone development.
