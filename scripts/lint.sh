#!/bin/bash
# Run ruff lint + format check.
# Forwards extra args to `ruff check`, e.g. ./scripts/lint.sh --fix
set -e
uv run --group dev ruff check "$@"
uv run --group dev ruff format --check
