# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository documents lessons learned from a career break focused on generative AI.

## Development Setup

### DevContainer Option (Recommended)

This project supports VS Code Dev Containers for a zero-configuration development experience:

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and [VS Code Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2. Open project in VS Code
3. Click "Reopen in Container" when prompted
4. Wait for build (~5 minutes first time)
5. Run `gh auth login` to authenticate with GitHub

The devcontainer provides:
- Python 3.13 + 3.14 (via pyenv) for tox multi-version testing
- Poetry 2.2.1 with all dependencies pre-installed
- Docker-in-Docker for Trivy security scanning
- GitHub CLI for Git authentication (`gh auth login`)
- All VS Code extensions pre-configured
- Pre-commit hooks ready to use

### Manual Setup Prerequisites

- Python 3.13+ (managed via pyenv, see `.python-version`)
- Poetry 2.2.1+
- Docker (optional - required only for `invoke trivy.check` and `invoke devcontainer.check`)
- Node.js (optional - required only for `invoke devcontainer.check`)

### Initial Setup

```bash
# Install Poetry (if not already installed)
make install_poetry

# Install dependencies and set up development environment
make install_ci

# For interactive development
make install_dev
```

### Windows Setup Notes

The project is cross-platform compatible with Windows, macOS, and Linux. Windows users have several options for running Make commands:

**Option 1: Install Make via Chocolatey (Recommended)**
```powershell
choco install make
```

**Option 2: Run Commands Directly**
Instead of `make install_ci`, run:
```powershell
poetry install
poetry run pre-commit install
```

Instead of `make install_dev`, run:
```powershell
poetry install
poetry run pre-commit install
poetry shell
invoke --list
```

**Option 3: Use WSL (Windows Subsystem for Linux)**
All commands will work natively in WSL Ubuntu.

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
- `invoke trivy.check` - Run comprehensive security scanning (vulnerabilities, secrets, misconfigurations, licenses)
- `invoke vulture.check` - Check for unused code
- `invoke xenon.check` - Check code complexity
- `invoke deptry.check` - Check for unused dependencies
- `invoke devcontainer.check` - Verify devcontainer builds and runs in headless mode
  - `--build-only`: Only build the image (fast check)
  - `--run-project-check`: Run full `invoke project.check` inside container

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

## Project Structure

```
.
├── .github/                      # GitHub Actions workflows and configuration
│   ├── workflows/
│   │   ├── main.yml             # CI pipeline for main branch
│   │   └── pr.yml               # CI pipeline for pull requests
│   ├── actions/                 # Reusable GitHub Actions
│   │   ├── ci-steps/            # Composite action for CI steps
│   │   ├── devcontainer-check/  # Composite action for devcontainer verification
│   │   └── multi-python-tests/  # Composite action for multi-Python testing
│   └── dependabot.yml           # Automated dependency updates
├── .quality/                     # Cache and temp files for various tools
│   ├── mypy/cache/              # MyPy cache
│   ├── ruff/cache/              # Ruff cache
│   ├── pytest/cache/            # Pytest cache
│   └── trivy/                   # Trivy cache
├── project/                      # Invoke task definitions (organized by tool)
│   ├── project.py               # Top-level tasks (project.check, project.update)
│   ├── project_task_runner.py   # Task runner infrastructure
│   ├── utils.py                 # Cross-platform utility functions
│   └── tasks/                   # Individual tool task modules
│       ├── actionlint.py        # GitHub Actions linting tasks
│       ├── deptry.py            # Dependency checking tasks
│       ├── devcontainer.py      # Devcontainer verification tasks
│       ├── mypy.py              # Type checking tasks
│       ├── pipaudit.py          # Security audit tasks
│       ├── poetry.py            # Poetry management tasks
│       ├── precommit.py         # Pre-commit hook tasks
│       ├── ruff.py              # Linting/formatting tasks
│       ├── testing.py           # Test execution tasks
│       ├── trivy.py             # Trivy security scanning tasks
│       ├── vulture.py           # Dead code detection tasks
│       └── xenon.py             # Complexity checking tasks
├── src/lessons_learnt/           # Main package source code
│   ├── __init__.py              # Package exports
│   ├── example.py               # Example module
│   └── py.typed                 # PEP 561 type hints marker
├── tests/
│   ├── unit/                    # Unit tests (80% coverage required)
│   └── integration/             # Integration tests (70% coverage required)
├── tasks.py                      # Invoke task collection entrypoint
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

### Invoke Task Architecture

The task system is organized hierarchically:

1. **Root entrypoint** (`tasks.py`): Imports and registers all task collections
2. **Project-level tasks** (`project/project.py`): Orchestrates multiple tools
   - `project.check`: Runs all quality checks in sequence (supports `--skip` and `--apply-safe-fixes`)
   - `project.update`: Updates all dependencies and pre-commit hooks
3. **Tool-specific tasks** (`project/tasks/*.py`): Individual tool operations
   - Each module exports a Collection with tool-specific tasks
   - All `context.run()` commands use `echo=True` to display commands being executed
4. **Task runner** (`project/project_task_runner.py`): Executes tasks with skipping support
5. **Cross-platform utilities** (`project/utils.py`): Platform-agnostic helper functions
   - `ensure_directory()`: Cross-platform replacement for `mkdir -p`
   - `get_current_working_directory()`: Cross-platform replacement for `$(pwd)`

### Cross-Platform Compatibility

The project codebase uses cross-platform compatible code patterns, though CI testing is performed on Ubuntu only. Users on other platforms should use the DevContainer for development.

- **No shell-specific commands**: All tasks use Python's `pathlib` and standard library instead of bash/shell commands
- **Path handling**: Uses `Path` objects that automatically handle OS-specific path separators
- **Docker paths**: Absolute paths with `Path.cwd().resolve()` work correctly on Docker Desktop for Windows
- **Utility functions**: `project/utils.py` provides cross-platform replacements for common shell operations

**When adding new tasks**:
- ❌ Avoid: `context.run("mkdir -p dir")` (Unix-only)
- ✅ Use: `ensure_directory("dir")` (cross-platform)
- ❌ Avoid: `context.run(f"cmd -v $(pwd)")` (bash-only)
- ✅ Use: `get_current_working_directory()` (cross-platform)

### Dependency Philosophy

- **Minimal runtime dependencies**: Only `invoke` for task automation
- **Comprehensive dev dependencies**: 17 development tools for quality, testing, and security
- **Poetry plugin requirement**: `poetry-plugin-export` for pip-audit compatibility

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
  - Type hints required for all functions (enforced by ruff ANN rules)

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
  - Additional plugins: pytest-mock

### Security

- **Pre-commit hooks**: Automated checks including:
  - Gitleaks: Secret detection
  - AWS credentials detection
  - Private key detection
  - Code quality checks
  - No direct commits to main/master branches

- **Pip-audit**: Vulnerability scanning for dependencies

- **Trivy**: Comprehensive security scanner
  - Runs in Docker container (`aquasec/trivy`)
  - Scans filesystem for multiple security issues
  - Scanners enabled: vulnerabilities, secrets, misconfigurations, licenses
  - Exits with error code 1 if any issues are found
  - Cache stored in `.quality/trivy/`

## CI/CD Pipeline

### GitHub Actions Workflows

- **main.yml**: Runs on push to main branch
  - Executes all CI steps via composite action
  - Runs unit and integration tests on Python 3.13 and 3.14
  - Tests on `ubuntu-latest` only

- **pr.yml**: Runs on all pull requests
  - Same test matrix as main branch (2 Python versions on Ubuntu)
  - Concurrent runs with cancellation of in-progress jobs
  - Includes PR write permissions for comments
  - Devcontainer check with path-based triggering (full check only when relevant files change)

- **devcontainer-weekly.yml**: Scheduled weekly (Sundays 6am UTC)
  - Full devcontainer verification to catch external drift (base image updates, dependency changes)
  - Can be manually triggered via workflow_dispatch

- **claude.yml**: Claude Code GitHub integration
  - Responds to `@claude` mentions in issue comments, PR review comments, and issues
  - Requires `CLAUDE_CODE_OAUTH_TOKEN` secret

- **claude-code-review.yml**: Automatic Claude Code review on PRs
  - Triggers on PR open, synchronize, ready_for_review, and reopened events
  - Uses the `code-review` plugin from Claude Code plugins marketplace

### Composite Actions

- **ci-steps**: Runs actionlint, Python setup, poetry install, and `invoke project.check`
- **devcontainer-check**: Builds and verifies devcontainer (supports quick build-only or full verification)
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

- **Cross-platform compatibility is mandatory**: Use `project/utils.py` functions instead of shell commands
- **All `context.run()` commands in tasks use `echo=True`** to display commands being executed
- **Socket access is disabled in tests** to prevent accidental network calls
- **Poetry checks are temporarily disabled** in pre-commit due to GitHub Actions v2.2.1 compatibility
- **Actionlint runs via pre-commit** and CI composite action (not as an invoke task)
- **Type hints are required** for all functions (enforced by ruff ANN rules)
- **Line length is 120 characters** (different from common 88/100 defaults)
- **CI/CD tests on Ubuntu only**: Use DevContainer for development on other platforms
