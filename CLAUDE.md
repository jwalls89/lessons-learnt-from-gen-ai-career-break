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

### Running Individual Tests

```bash
# Run a specific test file
poetry run pytest tests/unit/test_example.py

# Run a specific test class
poetry run pytest tests/unit/test_example.py::TestGreet

# Run a specific test method
poetry run pytest tests/unit/test_example.py::TestGreet::test_greet_with_valid_name

# Run tests matching a pattern
poetry run pytest -k "test_greet"

# Run tests with verbose output
poetry run pytest -v

# Run tests marked as slow
poetry run pytest -m slow

# Run tests excluding slow ones
poetry run pytest -m "not slow"
```

### Make Commands

- `make install_poetry` - Install Poetry and plugins
- `make install_ci` - Install dependencies and pre-commit hooks
- `make install_dev` - Full development setup with shell activation

## Code Quality Standards

### Linting & Formatting

- **Ruff**: Primary linter and formatter (replaces black, isort, flake8)
  - Line length: 120 characters
  - Target Python version: 3.13
  - Indent width: 4 spaces
  - Quote style: double quotes
  - Comprehensive rule set: 40+ categories including security (bandit), complexity, best practices
  - Extended safe fixes for: ANN201, ANN202, ANN204, E712, EM101, EM102, PLC0414, PT006, TC001, TC003
  - Test files exempted from: docstrings (D), assert statements (S101), magic values (PLR2004), boolean traps (FBT001)
  - Ignored rules: COM812, ISC001 (formatter compatibility), G004, TRY300 (personal choices), D203, D213 (PEP 257 convention)
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
  - Ignores pydantic decorators: `@model_validator`, `@field_serializer`, `@field_validator`
  - Ignores pytest fixtures: `@pytest.fixture`
  - Ignores common patterns: `visit_*`, `model_post_init`, `model_config`, `side_effect`, `return_value`, `__enter__`, `__exit__`

- **Deptry**: Dependency checker
  - Detects unused or missing dependencies
  - Knows `lessons_learnt` as first-party package

### Testing

- **Pytest**: Test framework
  - Unit tests: `tests/unit/` (80% coverage required)
  - Integration tests: `tests/integration/` (70% coverage required)
  - Socket access disabled during tests (via pytest-socket)
  - Coverage reports stored in `.quality/pytest-cov/`
  - Test markers available:
    - `slow`: Mark slow tests (deselect with `-m "not slow"`)
    - `order`: Control test execution order (via pytest-order)
  - Additional plugins: pytest-mock, pytest-unordered, pyfakefs, polyfactory, freezegun

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
├── .github/                      # GitHub Actions workflows and configuration
│   ├── workflows/
│   │   ├── main.yml             # CI pipeline for main branch
│   │   └── pr.yml               # CI pipeline for pull requests
│   ├── actions/                 # Reusable GitHub Actions
│   └── dependabot.yml           # Automated dependency updates
├── .quality/                     # Cache and temp files for various tools
│   ├── mypy/cache/              # MyPy cache
│   ├── ruff/cache/              # Ruff cache
│   └── pytest/cache/            # Pytest cache
├── src/lessons_learnt/           # Main package source code
│   ├── __init__.py              # Package exports
│   ├── example.py               # Example module
│   └── py.typed                 # PEP 561 type hints marker
├── tests/
│   ├── unit/                    # Unit tests (80% coverage required)
│   └── integration/             # Integration tests (70% coverage required)
├── tasks.py                      # Invoke task definitions
├── pyproject.toml               # Poetry dependencies and tool configuration
├── Makefile                     # Common setup commands
├── .pre-commit-config.yaml      # Pre-commit hook configuration
├── .python-version              # Python version specification (3.13.1, 3.14.0)
├── .unit-test-coveragerc        # Unit test coverage configuration
├── .integration-test-coveragerc # Integration test coverage configuration
├── vulture_whitelist            # Vulture dead code exclusions
└── CLAUDE.md                    # This file
```

## Code Architecture

### Package Organization

- **Package name**: `lessons_learnt` (source in `src/lessons_learnt/`)
- **Package mode**: Enabled with `py.typed` marker for PEP 561 compliance
- **Module exports**: Controlled via `__init__.py` (only exports what's intended for public API)
- **First-party detection**: Configured in deptry as `lessons_learnt`

### Dependency Philosophy

- **Minimal runtime dependencies**: Only `invoke` for task automation
- **Comprehensive dev dependencies**: 17 development tools for quality, testing, and security
- **Poetry plugin requirement**: `poetry-plugin-export` for pip-audit compatibility

## CI/CD Pipeline

### GitHub Actions Workflows

- **main.yml**: Runs on push to main branch
  - Executes all CI steps via composite action
  - Runs unit and integration tests on Python 3.13
  - Python 3.14 support pending GitHub Actions update

- **pr.yml**: Runs on all pull requests
  - Same test matrix as main branch
  - Concurrent runs with cancellation of in-progress jobs
  - Includes PR write permissions for comments

### Composite Actions

- **ci-steps**: Runs actionlint, Python setup, poetry install, and `invoke project.check`
- **multi-python-tests**: Runs unit and integration tests on specified Python version

### Dependabot

- Weekly updates for pip packages and GitHub Actions
- Targets main branch with "chore" commit prefix

## Development Workflow

1. Make changes to code/documentation
2. Run `invoke project.check --apply-safe-fixes` to validate and auto-fix issues
3. Commit changes (pre-commit hooks will run automatically)
4. Pre-commit hooks prevent commits to main/master branches directly
5. Push to feature branch and create pull request
6. CI/CD pipeline runs all checks automatically

## Important Notes

- **All `context.run()` commands in tasks.py use `echo=True`** to display commands being executed
- **Socket access is disabled in tests** to prevent accidental network calls
- **Poetry checks are temporarily disabled** in pre-commit due to GitHub Actions v2.2.1 compatibility
- **Actionlint check exists** but not yet integrated into main CI workflow
- **Type hints are required** for all functions (enforced by ruff ANN rules)
- **Line length is 120 characters** (different from common 88/100 defaults)
