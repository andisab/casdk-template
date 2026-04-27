# Skills Directory

This directory contains reusable [Skills](https://code.claude.com/docs/en/agent-sdk/skills) that subagents can load to access specialized knowledge, formatting guidelines, or domain-specific instructions.

## What are Skills?

Skills are modular knowledge packages that provide agents with:
- Domain-specific expertise and best practices
- Formatting and style guidelines
- Template structures and patterns
- Specialized instructions for specific tasks

They are loaded on demand by an agent calling the `Skill` tool — not pre-injected into the system prompt — so they don't bloat context until needed.

## Structure

Each skill is a subdirectory with at minimum a `SKILL.md` file; optional supporting resources go under `resources/`:

```
.claude/skills/
└── skill-name/
    ├── SKILL.md
    └── resources/          # Optional supporting files
        └── ...
```

## Bundled Skills

This template ships with two skills as a worked example of the **routing-skill → formatting-skill** pattern:

- **`joplin-research/`** — research-content templates (technical surveys, rundowns, book/article/whitepaper summaries) and citation standards. Routes to the right template based on the user's request type. Delegates all markdown formatting to `joplin-formatting`.
- **`joplin-formatting/`** — Joplin-compatible markdown rules (heading hierarchy, spacing, link styling, callouts). Invoked by `joplin-research` and usable on its own for any Joplin-bound output.

The `report-writer` subagent in `agents/agent.py` declares both via `skills=["joplin-research", "joplin-formatting"]` so the chained skill load works.

## Critical: Subagents Do NOT Inherit Project Skills Automatically

Even with `setting_sources=["project"]` on `ClaudeAgentOptions`, **subagents only see skills that are explicitly listed in their `AgentDefinition.skills` field.** This is a common source of "the skill is in `.claude/skills/` but the subagent never loads it" bugs.

```python
AgentDefinition(
    description=...,
    prompt=...,
    tools=["Skill", "Read", "Write"],  # Skill tool must be allowed
    skills=["your-skill-name"],         # Skill must be declared here
)
```

If your skill delegates to another skill (as `joplin-research` does to `joplin-formatting`), **both skill names must be in the same `skills=[…]` list.**

## Creating a Skill

1. Create a subdirectory with your skill name (use kebab-case):
   ```bash
   mkdir -p .claude/skills/my-skill-name
   ```

2. Create a `SKILL.md` file with your guidelines, templates, or instructions:
   ```markdown
   # My Skill Name

   ## Purpose
   Brief description of what this skill provides.

   ## Guidelines
   Detailed instructions, templates, or best practices.

   ## Examples
   Code examples, formatting samples, or use cases.
   ```

3. (Optional) Add supporting files under `resources/`:
   ```bash
   mkdir -p .claude/skills/my-skill-name/resources
   ```

4. Declare the skill on every subagent that should be able to load it:
   ```python
   AgentDefinition(..., skills=["my-skill-name"])
   ```

5. Reference the skill in the subagent's prompt so it knows when to load:
   ```
   Load the "my-skill-name" skill for guidelines on [task].
   ```

## Tips

- Keep each skill focused on a single domain or task type
- Use clear, actionable language in guidelines
- Include examples wherever possible
- Skills can reference other skills, but each must be declared on the subagent
- Use progressive disclosure: short `SKILL.md` that points at deeper files in `resources/`

## See Also

- [Claude Agent SDK – Python](https://code.claude.com/docs/en/agent-sdk/python)
- [Claude Agent SDK – Subagents guide](https://code.claude.com/docs/en/agent-sdk/subagents)
- `agents/prompts/` — agent system prompts that may reference skills
- `CLAUDE.md` — project context and architecture
