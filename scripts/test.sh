#!/bin/bash
# Run the test suite.
# Forwards extra args to pytest, e.g. ./scripts/test.sh -k message_handler -vv
set -e
uv run --group dev pytest "$@"
