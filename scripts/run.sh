#!/bin/bash
# Quick run script for research agent

set -e

# Check if .env exists and has API key
if [ ! -f .env ]; then
    echo "Error: .env file not found."
    echo "Run ./scripts/setup.sh first"
    exit 1
fi

# Check if ANTHROPIC_API_KEY is set in .env
if ! grep -q "^ANTHROPIC_API_KEY=.\\+" .env; then
    echo "Error: ANTHROPIC_API_KEY not set in .env file"
    echo "Edit .env and add your API key"
    echo "Get your key at: https://console.anthropic.com/settings/keys"
    exit 1
fi

echo "Starting Research Agent..."
echo ""

uv run agents/agent.py
