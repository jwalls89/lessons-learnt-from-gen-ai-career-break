#!/bin/bash
set -e

echo "========================================"
echo "  Dev Container Post-Create Setup"
echo "========================================"

# Configure pyenv for this project
echo ""
echo "=== Configuring pyenv for project ==="
pyenv local 3.13.1 3.14.0

# Configure Poetry to create venv in project
echo ""
echo "=== Configuring Poetry ==="
poetry config virtualenvs.in-project true

# Install dependencies
echo ""
echo "=== Installing project dependencies ==="
poetry install

# Install pre-commit hooks
echo ""
echo "=== Installing pre-commit hooks ==="
poetry run pre-commit install

# Install Claude Code CLI
echo ""
echo "=== Installing Claude Code CLI ==="
# Fix npm cache permissions (may have root-owned files from devcontainer build)
sudo chown -R "$(id -u):$(id -g)" ~/.npm 2>/dev/null || true
npm install -g @anthropic-ai/claude-code

# Validation
echo ""
echo "========================================"
echo "  Validating Setup"
echo "========================================"
echo "Python version: $(python --version)"
echo "Poetry version: $(poetry --version)"
echo "Docker version: $(docker --version)"
echo "Claude Code version: $(claude --version)"
echo ""
echo "Available Python versions:"
pyenv versions
echo ""
echo "Available invoke tasks:"
poetry run invoke --list

echo ""
echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo ""
