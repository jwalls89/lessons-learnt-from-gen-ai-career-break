# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository documents lessons learned from a career break focused on generative AI.

## Development Setup

### Prerequisites

- Python 3.13+ (managed via pyenv, see `.python-version`)
- Poetry 2.2.1+

### Initial Setup

```bash
# Install Poetry (if not already installed)
make install_poetry

# Install dependencies and set up development environment
make install_ci

# For interactive development
make install_dev
```

## Common Commands

### Poetry Commands

- `poetry install` - Install all dependencies
- `poetry update` - Update all dependencies
- `poetry shell` - Activate the virtual environment
- `poetry add <package>` - Add a new dependency
- `poetry add --group dev <package>` - Add a development dependency

### Invoke Tasks

The project uses `invoke` for task automation. View all available tasks:
```bash
invoke --list
```

Key tasks:
- `invoke project.check` - Run all project checks (linting, type checking, tests, security)
- `invoke project.update` - Update all dependencies and pre-commit hooks
- `invoke ruff.lint` - Run ruff linting (use `--apply-safe-fixes` to auto-fix)
- `invoke ruff.format` - Run ruff formatting (use `--apply-safe-fixes` to auto-format)
- `invoke mypy.check` - Run type checking
- `invoke precommit.check` - Run pre-commit hooks
- `invoke tests.unit` - Run unit tests
- `invoke tests.integration` - Run integration tests
- `invoke tests.tox` - Run multi-version testing
- `invoke pipaudit.check` - Check for vulnerable dependencies
- `invoke vulture.check` - Check for unused code
- `invoke xenon.check` - Check code complexity
- `invoke deptry.check` - Check for unused dependencies
- `invoke actionlint.check` - Check GitHub Actions workflows

### Make Commands

- `make install_poetry` - Install Poetry and plugins
- `make install_ci` - Install dependencies and pre-commit hooks
- `make install_dev` - Full development setup with shell activation

## Code Quality Standards

### Linting & Formatting

- **Ruff**: Primary linter and formatter
  - Line length: 120 characters
  - Target Python version: 3.13
  - Comprehensive rule set covering code style, security, complexity, and best practices
  - Configuration in `pyproject.toml`

### Type Checking

- **MyPy**: Static type checker
  - Cache directory: `.quality/mypy/cache`
  - Excludes: `vulture_whitelist`, `tasks.py`

### Code Quality Tools

- **Xenon**: Code complexity analyzer
  - Max absolute complexity: B
  - Max module complexity: A
  - Max average complexity: A

- **Vulture**: Dead code detector
  - Excludes: `.quality`, `.poetry`

- **Deptry**: Dependency checker
  - Detects unused or missing dependencies

### Testing

- **Pytest**: Test framework
  - Unit tests: `tests/unit/` (80% coverage required)
  - Integration tests: `tests/integration/` (70% coverage required)
  - Socket access disabled during tests
  - Coverage reports stored in `.quality/pytest-cov/`

### Security

- **Pre-commit hooks**: Automated checks including:
  - Gitleaks: Secret detection
  - AWS credentials detection
  - Private key detection
  - Code quality checks

- **Pip-audit**: Vulnerability scanning for dependencies

## Project Structure

```
.
├── .quality/                 # Cache and temp files for various tools
├── tasks.py                  # Invoke task definitions
├── pyproject.toml           # Poetry dependencies and tool configuration
├── Makefile                 # Common setup commands
├── .pre-commit-config.yaml  # Pre-commit hook configuration
├── .python-version          # Python version specification for pyenv
├── .unit-test-coveragerc    # Unit test coverage configuration
├── .integration-test-coveragerc  # Integration test coverage configuration
└── CLAUDE.md                # This file
```

## Development Workflow

1. Make changes to code/documentation
2. Run `invoke project.check --apply-safe-fixes` to validate and auto-fix issues
3. Commit changes (pre-commit hooks will run automatically)
4. Pre-commit hooks prevent commits to main/master branches directly
