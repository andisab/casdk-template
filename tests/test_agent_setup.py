"""Behavioral tests for agent.py module-level setup.

These exercise the build_agents() and build_options() factories so we can
assert on the constructed AgentDefinition / ClaudeAgentOptions objects
instead of grepping the source.
"""

from types import SimpleNamespace

from claude_agent_sdk import AgentDefinition, ClaudeAgentOptions

from agents.agent import (
    _accumulate_result,
    _format_totals,
    build_agents,
    build_options,
    load_prompt,
)

# --- module-level smoke ---------------------------------------------------


def test_agent_module_imports_cleanly():
    """If imports break, the user can't even start the agent."""
    import agents.agent  # noqa: F401


def test_load_prompt_reads_each_prompt_file():
    for name in ("lead_agent.txt", "researcher.txt", "report_writer.txt"):
        content = load_prompt(name)
        assert isinstance(content, str)
        assert content.strip(), f"{name} loaded as empty"


# --- build_agents() -------------------------------------------------------


def _agents() -> dict[str, AgentDefinition]:
    return build_agents(researcher_prompt="r-prompt", report_writer_prompt="rw-prompt")


def test_build_agents_returns_two_subagents():
    agents = _agents()
    assert set(agents.keys()) == {"researcher", "report-writer"}
    assert all(isinstance(d, AgentDefinition) for d in agents.values())


def test_researcher_has_websearch_and_write_only():
    agents = _agents()
    assert agents["researcher"].tools == ["WebSearch", "Write"]


def test_researcher_prompt_is_passed_through():
    agents = _agents()
    assert agents["researcher"].prompt == "r-prompt"


def test_report_writer_has_skill_read_write_glob_tools():
    agents = _agents()
    assert set(agents["report-writer"].tools or []) == {"Skill", "Write", "Glob", "Read"}


def test_report_writer_declares_joplin_research_and_formatting_skills():
    """Regression: subagents do not inherit project skills automatically.

    joplin-research delegates markdown formatting to joplin-formatting, so the
    report-writer must declare both for the chained skill load to work.
    """
    agents = _agents()
    skills = agents["report-writer"].skills or []
    assert "joplin-research" in skills
    assert "joplin-formatting" in skills


def test_subagents_have_max_turns_cap():
    """Both subagents should declare maxTurns to prevent runaway loops."""
    agents = _agents()
    assert agents["researcher"].maxTurns == 10
    assert agents["report-writer"].maxTurns == 5


def test_subagents_cannot_spawn_other_subagents():
    """Per SDK docs: subagents cannot spawn subagents. Don't include Agent/Task in their tools."""
    agents = _agents()
    for name, defn in agents.items():
        tools = defn.tools or []
        assert "Agent" not in tools, f"{name} must not have Agent in tools"
        assert "Task" not in tools, f"{name} must not have Task in tools"


# --- build_options() ------------------------------------------------------


def _options(agents: dict[str, AgentDefinition] | None = None) -> ClaudeAgentOptions:
    return build_options(
        system_prompt="lead",
        agents=agents if agents is not None else _agents(),
    )


def test_build_options_allows_both_agent_and_task():
    """Regression: subagent tool was renamed Task -> Agent in Claude Code v2.1.63."""
    options = _options()
    assert "Agent" in options.allowed_tools
    assert "Task" in options.allowed_tools


def test_build_options_uses_bypass_permissions_default():
    """The README's safety warning is anchored to this default. Change one, change both."""
    options = _options()
    assert options.permission_mode == "bypassPermissions"


def test_build_options_loads_project_setting_sources():
    """setting_sources=['project'] is required for project CLAUDE.md / settings to load."""
    options = _options()
    assert options.setting_sources == ["project"]


def test_build_options_does_not_set_cli_path():
    """Regression: ~50 LOC of brittle CLI path discovery was removed.

    The SDK locates the CLI on $PATH on its own; our code must not pin cli_path.
    """
    options = _options()
    assert options.cli_path is None


def test_build_options_passes_system_prompt_through():
    options = build_options(system_prompt="<lead-prompt>", agents=_agents())
    assert options.system_prompt == "<lead-prompt>"


def test_build_options_attaches_agents():
    agents = _agents()
    options = build_options(system_prompt="lead", agents=agents)
    assert options.agents is agents


def test_build_options_uses_haiku_model_default():
    options = _options()
    assert options.model == "haiku"


# --- ResultMessage accumulation ------------------------------------------


def _result(**kwargs) -> SimpleNamespace:
    """Build a ResultMessage-shaped object using duck typing.

    Real ResultMessage requires many positional fields; SimpleNamespace lets
    us assert the accumulator only touches the attributes it claims to.
    """
    defaults: dict = {
        "num_turns": 0,
        "total_cost_usd": None,
        "usage": None,
    }
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


def test_accumulate_result_sums_turns_cost_and_tokens():
    totals = {"turns": 0, "cost_usd": 0.0, "input_tokens": 0, "output_tokens": 0}

    _accumulate_result(
        totals,
        _result(num_turns=3, total_cost_usd=0.01, usage={"input_tokens": 100, "output_tokens": 50}),
    )
    _accumulate_result(
        totals,
        _result(num_turns=2, total_cost_usd=0.02, usage={"input_tokens": 40, "output_tokens": 60}),
    )

    assert totals == {"turns": 5, "cost_usd": 0.03, "input_tokens": 140, "output_tokens": 110}


def test_accumulate_result_tolerates_missing_fields():
    """Cost/usage may legitimately be None; turns may be 0 — none of those should crash."""
    totals = {"turns": 0, "cost_usd": 0.0, "input_tokens": 0, "output_tokens": 0}
    _accumulate_result(totals, _result())
    assert totals == {"turns": 0, "cost_usd": 0.0, "input_tokens": 0, "output_tokens": 0}


def test_format_totals_renders_one_line_summary():
    out = _format_totals(
        {"turns": 4, "cost_usd": 0.0312, "input_tokens": 12847, "output_tokens": 3201}
    )
    assert out == "Session: 4 turns, $0.0312 USD, 12,847 input / 3,201 output tokens"
