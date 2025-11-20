#!/bin/bash
# Setup script for research agent

set -e

echo "=== Research Agent Setup ==="
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed."
    echo "Install uv with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "✓ uv is installed"

# Check if .env file exists
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your ANTHROPIC_API_KEY"
    echo "   Get your API key at: https://console.anthropic.com/settings/keys"
else
    echo "✓ .env file exists"
fi

# Sync dependencies
echo ""
echo "Installing dependencies with uv..."
uv sync

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your ANTHROPIC_API_KEY (if not already done)"
echo "  2. Run the agent with: ./scripts/run.sh"
echo "  3. Or use: uv run agents/agent.py"
echo ""
