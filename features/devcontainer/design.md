# Devcontainer Support - Design

## Overview

This document describes the technical design for adding devcontainer support to the project. The design follows the hybrid approach: Microsoft DevContainers base image with features for Docker-in-Docker and pyenv.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Host Machine                                 │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                    Docker Desktop / Docker CE                   │ │
│  │  ┌──────────────────────────────────────────────────────────┐  │ │
│  │  │                  Dev Container                            │  │ │
│  │  │                                                           │  │ │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐   │  │ │
│  │  │  │   Python    │  │   Poetry    │  │   Pre-commit    │   │  │ │
│  │  │  │ 3.13 + 3.14 │  │   2.2.1+    │  │     Hooks       │   │  │ │
│  │  │  │  (pyenv)    │  │             │  │                 │   │  │ │
│  │  │  └─────────────┘  └─────────────┘  └─────────────────┘   │  │ │
│  │  │                                                           │  │ │
│  │  │  ┌─────────────────────────────────────────────────────┐  │  │ │
│  │  │  │              Docker-in-Docker                        │  │  │ │
│  │  │  │  ┌─────────────────────────────────────────────┐    │  │  │ │
│  │  │  │  │           aquasec/trivy                      │    │  │  │ │
│  │  │  │  │        (pulled on demand)                    │    │  │  │ │
│  │  │  │  └─────────────────────────────────────────────┘    │  │  │ │
│  │  │  └─────────────────────────────────────────────────────┘  │  │ │
│  │  │                                                           │  │ │
│  │  │  ┌─────────────────────────────────────────────────────┐  │  │ │
│  │  │  │              /workspace (bind mount)                 │  │  │ │
│  │  │  │    Project files from host filesystem               │  │  │ │
│  │  │  └─────────────────────────────────────────────────────┘  │  │ │
│  │  └──────────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

## Components

### 1. Directory Structure

```
.devcontainer/
├── devcontainer.json    # Main configuration file
└── scripts/
    └── post-create.sh   # Post-creation setup script
```

### 2. Base Image Selection

**Choice**: `mcr.microsoft.com/devcontainers/base:ubuntu-24.04`

**Rationale**:
- Ubuntu Noble (24.04) provides latest base packages
- Using base image (not Python-specific) because we need pyenv for multi-version support
- Well-maintained by Microsoft with regular security updates
- Compatible with all DevContainer features

### 3. DevContainer Features

| Feature | Version | Purpose |
|---------|---------|---------|
| `ghcr.io/devcontainers/features/docker-in-docker` | latest | Enable Docker daemon for Trivy |
| `ghcr.io/devcontainers-extra/features/pyenv` | latest | Install Python 3.13.1 and 3.14.0 |
| `ghcr.io/devcontainers/features/common-utils` | latest | Git, curl, and common utilities |

### 4. devcontainer.json Structure

```json
{
    "name": "lessons-learnt-from-gen-ai-career-break",
    "image": "mcr.microsoft.com/devcontainers/base:ubuntu-24.04",

    "features": {
        "ghcr.io/devcontainers/features/docker-in-docker:2": {
            "dockerDashComposeVersion": "v2"
        },
        "ghcr.io/devcontainers-extra/features/pyenv:2": {
            "version": "latest"
        },
        "ghcr.io/devcontainers/features/common-utils:2": {
            "installZsh": false,
            "installOhMyZsh": false,
            "configureZshAsDefaultShell": false
        }
    },

    "postCreateCommand": ".devcontainer/scripts/post-create.sh",

    "customizations": {
        "vscode": {
            "settings": { ... },
            "extensions": [ ... ]
        }
    }
}
```

## Detailed Component Design

### 5. Post-Create Script

**File**: `.devcontainer/scripts/post-create.sh`

**Purpose**: Configure Python environment, install Poetry, and set up project dependencies.

**Execution Flow**:

```
┌─────────────────────────────────────────┐
│         post-create.sh                  │
├─────────────────────────────────────────┤
│ 1. Install Python 3.13.1 via pyenv      │
│ 2. Install Python 3.14.0 via pyenv      │
│ 3. Set Python 3.13.1 as global default  │
│ 4. Install Poetry via pipx              │
│ 5. Add poetry-plugin-export             │
│ 6. Run poetry install                   │
│ 7. Run pre-commit install               │
└─────────────────────────────────────────┘
```

**Script Content**:

```bash
#!/bin/bash
set -e

echo "=== Installing Python versions via pyenv ==="
pyenv install 3.13.1
pyenv install 3.14.0
pyenv global 3.13.1
pyenv local 3.13.1 3.14.0

echo "=== Installing Poetry ==="
pipx install poetry==2.2.1
pipx inject poetry poetry-plugin-export

echo "=== Installing project dependencies ==="
poetry install

echo "=== Installing pre-commit hooks ==="
poetry run pre-commit install

echo "=== Setup complete ==="
```

### 6. VS Code Settings

**Settings to configure**:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.terminal.activateEnvironment": true,

    "[python]": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.codeActionsOnSave": {
            "source.fixAll.ruff": "explicit",
            "source.organizeImports.ruff": "explicit"
        }
    },

    "ruff.lineLength": 120,
    "ruff.lint.args": ["--config=pyproject.toml"],
    "ruff.format.args": ["--config=pyproject.toml"],

    "files.exclude": {
        "**/__pycache__": true,
        "**/.pytest_cache": true,
        "**/.mypy_cache": true,
        "**/.ruff_cache": true,
        ".quality": true
    }
}
```

### 7. VS Code Extensions

**Extension IDs** (15 total):

```json
[
    // Python Development
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.debugpy",
    "ms-python.vscode-python-envs",
    "charliermarsh.ruff",

    // Project Utilities
    "ms-vscode.makefile-tools",
    "redhat.vscode-yaml",
    "github.vscode-github-actions",

    // AI Assistants
    "anthropic.claude-code",
    "github.copilot",
    "github.copilot-chat",
    "amazonwebservices.amazon-q-vscode",

    // AWS Development
    "amazonwebservices.aws-toolkit-vscode",
    "boto3typed.boto3-ide",

    // Documentation
    "vstirbu.vscode-mermaid-preview"
]
```

## Data Flow

### Container Startup Sequence

```
User opens project in VS Code
           │
           ▼
VS Code detects .devcontainer/devcontainer.json
           │
           ▼
User prompted: "Reopen in Container"
           │
           ▼
┌──────────────────────────────────────────┐
│         Docker Image Build               │
│  1. Pull base image (ubuntu-24.04)       │
│  2. Install Docker-in-Docker feature     │
│  3. Install pyenv feature                │
│  4. Install common-utils feature         │
└──────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│         Post-Create Command              │
│  1. pyenv install 3.13.1                 │
│  2. pyenv install 3.14.0                 │
│  3. pipx install poetry                  │
│  4. poetry install                       │
│  5. pre-commit install                   │
└──────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│         VS Code Initialization           │
│  1. Install extensions                   │
│  2. Apply settings                       │
│  3. Configure Python interpreter         │
└──────────────────────────────────────────┘
           │
           ▼
Development environment ready
```

### Invoke Task Execution

```
Developer runs: invoke project.check
           │
           ▼
┌──────────────────────────────────────────┐
│  Poetry virtual environment activated    │
│  via poetry run                          │
└──────────────────────────────────────────┘
           │
           ├──► invoke ruff.lint
           ├──► invoke ruff.format
           ├──► invoke mypy.check
           ├──► invoke tests.unit
           ├──► invoke tests.integration
           ├──► invoke vulture.check
           ├──► invoke xenon.check
           ├──► invoke deptry.check
           ├──► invoke pipaudit.check
           ├──► invoke precommit.check
           │
           ▼
┌──────────────────────────────────────────┐
│  invoke trivy.check                      │
│  └──► docker run aquasec/trivy           │
│       (uses Docker-in-Docker)            │
└──────────────────────────────────────────┘
```

## Error Handling

### Scenario 1: Docker-in-Docker Fails to Start

**Detection**: `docker ps` returns error in container

**Mitigation**:
- Post-create script checks Docker daemon status
- Provides clear error message with troubleshooting steps
- User can skip Trivy with `invoke project.check --skip trivy.check`

### Scenario 2: pyenv Installation Fails

**Detection**: `pyenv install` returns non-zero exit code

**Mitigation**:
- Script uses `set -e` to fail fast
- Error message includes pyenv build dependencies
- User can rebuild container to retry

### Scenario 3: Poetry Install Fails

**Detection**: `poetry install` returns non-zero exit code

**Causes**:
- Network issues
- Incompatible dependency versions

**Mitigation**:
- Poetry lock file is committed, ensuring reproducible builds
- Clear error output from Poetry
- User can run `poetry install` manually after investigating

### Scenario 4: Extension Fails to Install

**Detection**: VS Code shows extension installation error

**Mitigation**:
- Extensions are installed asynchronously, don't block container start
- User can install failed extensions manually
- Core functionality (Python, Ruff) works even if AI extensions fail

## Testing Strategy

### Manual Testing Checklist

| Test Case | Command/Action | Expected Result |
|-----------|---------------|-----------------|
| Container builds | Open in container | No build errors |
| Python 3.13 available | `python --version` | Python 3.13.1 |
| Python 3.14 available | `pyenv versions` | Lists 3.14.0 |
| Poetry works | `poetry --version` | 2.2.1+ |
| Dependencies installed | `poetry run invoke --list` | Shows all tasks |
| Unit tests pass | `invoke tests.unit` | Exit code 0 |
| Integration tests pass | `invoke tests.integration` | Exit code 0 |
| Tox multi-version | `invoke tests.tox` | Tests on 3.13 + 3.14 |
| Trivy works | `invoke trivy.check` | Docker runs Trivy |
| Full check passes | `invoke project.check` | All checks pass |
| Ruff extension | Open .py file | Linting works |
| Format on save | Edit and save .py | Auto-formatted |
| Pre-commit hooks | Make commit | Hooks run |

### Automated Validation

Add to post-create script:

```bash
echo "=== Validating setup ==="
python --version | grep "3.13"
poetry --version | grep "2.2"
docker --version
invoke --list
echo "=== Validation complete ==="
```

## Configuration Reference

### Complete devcontainer.json

```json
{
    "name": "lessons-learnt-from-gen-ai-career-break",
    "image": "mcr.microsoft.com/devcontainers/base:ubuntu-24.04",

    "features": {
        "ghcr.io/devcontainers/features/docker-in-docker:2": {
            "dockerDashComposeVersion": "v2",
            "moby": true
        },
        "ghcr.io/devcontainers-extra/features/pyenv:2": {
            "version": "latest"
        },
        "ghcr.io/devcontainers/features/common-utils:2": {
            "installZsh": false,
            "installOhMyZsh": false,
            "configureZshAsDefaultShell": false,
            "upgradePackages": true
        }
    },

    "postCreateCommand": "bash .devcontainer/scripts/post-create.sh",

    "customizations": {
        "vscode": {
            "settings": {
                "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
                "python.terminal.activateEnvironment": true,
                "[python]": {
                    "editor.formatOnSave": true,
                    "editor.defaultFormatter": "charliermarsh.ruff",
                    "editor.codeActionsOnSave": {
                        "source.fixAll.ruff": "explicit",
                        "source.organizeImports.ruff": "explicit"
                    }
                },
                "ruff.lineLength": 120,
                "ruff.lint.args": ["--config=pyproject.toml"],
                "ruff.format.args": ["--config=pyproject.toml"],
                "files.exclude": {
                    "**/__pycache__": true,
                    "**/.pytest_cache": true,
                    "**/.mypy_cache": true,
                    "**/.ruff_cache": true,
                    ".quality": true
                }
            },
            "extensions": [
                "ms-python.python",
                "ms-python.vscode-pylance",
                "ms-python.debugpy",
                "ms-python.vscode-python-envs",
                "charliermarsh.ruff",
                "ms-vscode.makefile-tools",
                "redhat.vscode-yaml",
                "github.vscode-github-actions",
                "anthropic.claude-code",
                "github.copilot",
                "github.copilot-chat",
                "amazonwebservices.amazon-q-vscode",
                "amazonwebservices.aws-toolkit-vscode",
                "boto3typed.boto3-ide",
                "vstirbu.vscode-mermaid-preview"
            ]
        }
    },

    "remoteUser": "vscode"
}
```

### Complete post-create.sh

```bash
#!/bin/bash
set -e

echo "========================================"
echo "  Dev Container Post-Create Setup"
echo "========================================"

# Install Python versions
echo ""
echo "=== Installing Python 3.13.1 ==="
pyenv install -s 3.13.1

echo ""
echo "=== Installing Python 3.14.0 ==="
pyenv install -s 3.14.0

# Configure pyenv
echo ""
echo "=== Configuring pyenv ==="
pyenv global 3.13.1
pyenv local 3.13.1 3.14.0

# Install Poetry
echo ""
echo "=== Installing Poetry 2.2.1 ==="
pipx install poetry==2.2.1
pipx inject poetry poetry-plugin-export

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

# Validation
echo ""
echo "========================================"
echo "  Validating Setup"
echo "========================================"
echo "Python version: $(python --version)"
echo "Poetry version: $(poetry --version)"
echo "Docker version: $(docker --version)"
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
echo "You can now run:"
echo "  invoke project.check    # Run all checks"
echo "  invoke tests.unit       # Run unit tests"
echo "  invoke tests.tox        # Run multi-version tests"
echo ""
```

## Documentation Updates

### README.md Addition

Add section after "Development Setup":

```markdown
### Development with DevContainer (Recommended)

The easiest way to set up a development environment is using VS Code Dev Containers:

**Prerequisites**:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/macOS) or Docker CE (Linux)
- [VS Code](https://code.visualstudio.com/) with [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

**Setup**:
1. Clone the repository
2. Open the folder in VS Code
3. When prompted, click "Reopen in Container"
4. Wait for the container to build (first time takes ~5 minutes)
5. Start developing!

The devcontainer includes:
- Python 3.13.1 and 3.14.0 (via pyenv)
- Poetry 2.2.1 with all dependencies
- Docker-in-Docker for Trivy security scanning
- Pre-configured VS Code extensions
- Pre-commit hooks installed
```

### CLAUDE.md Addition

Add to "Development Setup" section:

```markdown
### DevContainer Option

This project supports VS Code Dev Containers. Opening the project in a devcontainer provides:
- Pre-configured Python 3.13 + 3.14 environment
- All development dependencies installed
- Docker available for Trivy scanning
- VS Code extensions pre-installed

To use: Open in VS Code and select "Reopen in Container" when prompted.
```

## Security Considerations

1. **Docker-in-Docker Privileges**: The container runs with elevated privileges for DinD. This is acceptable for local development but means container isolation is reduced.

2. **Base Image Updates**: Microsoft base images receive regular security updates. Rebuilding the container (`Dev Containers: Rebuild Container`) pulls the latest image.

3. **Extension Trust**: All specified extensions are from verified publishers (Microsoft, Red Hat, GitHub, Anthropic, Amazon).

4. **No Secrets in Configuration**: The devcontainer configuration contains no secrets. User credentials (GitHub, AWS, etc.) are handled by VS Code credential forwarding.

## Performance Considerations

| Operation | Expected Time | Notes |
|-----------|---------------|-------|
| First container build | 3-5 minutes | Pulls base image + features |
| Post-create script | 2-3 minutes | pyenv builds Python from source |
| Subsequent startups | 10-30 seconds | Uses cached image |
| `poetry install` | 30-60 seconds | Uses cached venv |
| `invoke trivy.check` | 1-2 minutes | First run pulls Trivy image |

**Optimization Tips**:
- Docker Desktop resource allocation affects build speed
- Poetry's in-project venv is preserved across container rebuilds
- Trivy image is cached after first pull

## Dependencies

| Dependency | Version | Source |
|------------|---------|--------|
| Ubuntu | 24.04 (Noble) | Microsoft base image |
| Docker-in-Docker | v2 | DevContainer feature |
| pyenv | latest | DevContainer feature |
| Python | 3.13.1, 3.14.0 | Built by pyenv |
| Poetry | 2.2.1 | pipx |
| poetry-plugin-export | latest | pipx inject |

## Alternatives Considered

| Alternative | Reason Not Chosen |
|-------------|-------------------|
| Python-specific base image | Doesn't support multiple Python versions easily |
| deadsnakes PPA | Less portable than pyenv, Ubuntu-specific |
| Docker-outside-of-Docker | Shares host Docker state, less isolated |
| Custom Dockerfile | More maintenance burden, less benefit |
| Zsh + Oh My Zsh | Adds complexity, user can add if desired |
