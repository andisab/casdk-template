# Skills Directory

This directory contains reusable skills that agents can load to access specialized knowledge, formatting guidelines, or domain-specific instructions.

## What are Skills?

Skills are modular knowledge packages that provide agents with:
- Domain-specific expertise and best practices
- Formatting and style guidelines
- Template structures and patterns
- Specialized instructions for specific tasks

## Structure

Each skill is a subdirectory containing a `SKILL.md` file:

```
.claude/skills/
└── skill-name/
    └── SKILL.md
```

## Creating a Skill

1. Create a subdirectory with your skill name (use kebab-case):
   ```bash
   mkdir -p .claude/skills/my-skill-name
   ```

2. Create a `SKILL.md` file with your content:
   ```bash
   # My Skill Name

   ## Purpose
   Brief description of what this skill provides.

   ## Guidelines
   Detailed instructions, templates, or best practices.

   ## Examples
   Code examples, formatting samples, or use cases.
   ```

## Using Skills in Agents

Reference skills in agent prompts:

```
Load the "skill-name" skill for guidelines on [specific task].
```

The SDK automatically loads skills when `setting_sources=["project"]` is configured in `ClaudeAgentOptions`.

## Example Skills

### Research Formatting Skill
```
.claude/skills/research-formatting/
└── SKILL.md  # Contains citation formats, report structure templates
```

### Code Review Skill
```
.claude/skills/code-review-checklist/
└── SKILL.md  # Contains review criteria, common issues checklist
```

### Data Analysis Skill
```
.claude/skills/data-analysis-workflow/
└── SKILL.md  # Contains pandas patterns, visualization guidelines
```

## Configuration

Skills are loaded via the `setting_sources` option in `agents/agent.py`:

```python
options = ClaudeAgentOptions(
    setting_sources=["project"],  # Loads skills from .claude directory
    ...
)
```

## Tips

- Keep skills focused on a single domain or task type
- Use clear, actionable language in guidelines
- Include examples whenever possible
- Update skills based on what works in practice
- Skills can reference other skills if needed

## See Also

- [Claude Agent SDK Documentation](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-overview)
- `agents/prompts/` - Agent system prompts that may reference skills
- `CLAUDE.md` - Project context and architecture
