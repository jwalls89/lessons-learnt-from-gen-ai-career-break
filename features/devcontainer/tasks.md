# Devcontainer Support - Implementation Tasks

## Overview

This document provides a sequenced task breakdown for implementing devcontainer support. Tasks are ordered by dependencies and grouped into phases.

## Task Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| 1 | T1-T3 | Core devcontainer configuration |
| 2 | T4-T5 | Post-create setup script |
| 3 | T6-T7 | Testing and validation |
| 4 | T8-T9 | Documentation updates |

**Total Tasks**: 9

---

## Phase 1: Core Devcontainer Configuration

### T1: Create devcontainer directory structure

**Description**: Create the `.devcontainer` directory and subdirectories.

**Requirements**: FR-3.1 (VS Code prompts to reopen)

**Dependencies**: None

**Files to create**:
```
.devcontainer/
└── scripts/
```

**Commands**:
```bash
mkdir -p .devcontainer/scripts
```

**Acceptance Criteria**:
- [ ] `.devcontainer/` directory exists
- [ ] `.devcontainer/scripts/` directory exists

---

### T2: Create devcontainer.json

**Description**: Create the main devcontainer configuration file with base image, features, settings, and extensions.

**Requirements**: FR-1.1, FR-1.2, FR-2.1, FR-3.1, FR-3.2, FR-3.3, FR-3.4

**Dependencies**: T1

**File**: `.devcontainer/devcontainer.json`

**Content**:
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

**Acceptance Criteria**:
- [ ] File is valid JSON
- [ ] Base image is `mcr.microsoft.com/devcontainers/base:ubuntu-24.04`
- [ ] Docker-in-Docker feature is configured
- [ ] pyenv feature is configured
- [ ] All 15 extensions are listed
- [ ] VS Code settings match project configuration (line length 120, Ruff formatter)
- [ ] postCreateCommand points to setup script

---

### T3: Add .devcontainer to .gitignore exclusions (if needed)

**Description**: Ensure `.devcontainer` is NOT in `.gitignore` so it's committed to the repository.

**Requirements**: FR-3.1

**Dependencies**: T2

**Action**: Check `.gitignore` and ensure `.devcontainer` is not excluded.

**Acceptance Criteria**:
- [ ] `.devcontainer/` directory will be committed to git

---

## Phase 2: Post-Create Setup Script

### T4: Create post-create.sh script

**Description**: Create the shell script that runs after container creation to install Python versions, Poetry, and dependencies.

**Requirements**: FR-1.1, FR-1.2, FR-1.3, FR-1.4, FR-1.5, FR-1.6

**Dependencies**: T1

**File**: `.devcontainer/scripts/post-create.sh`

**Content**:
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

**Acceptance Criteria**:
- [ ] Script has executable shebang (`#!/bin/bash`)
- [ ] Script uses `set -e` for fail-fast behavior
- [ ] Installs Python 3.13.1 via pyenv
- [ ] Installs Python 3.14.0 via pyenv
- [ ] Sets pyenv global to 3.13.1
- [ ] Creates `.python-version` with both versions
- [ ] Installs Poetry 2.2.1 via pipx
- [ ] Injects poetry-plugin-export
- [ ] Configures Poetry for in-project virtualenv
- [ ] Runs `poetry install`
- [ ] Runs `pre-commit install`
- [ ] Outputs validation information

---

### T5: Make post-create.sh executable

**Description**: Ensure the post-create script has executable permissions.

**Requirements**: FR-1.5

**Dependencies**: T4

**Command**:
```bash
chmod +x .devcontainer/scripts/post-create.sh
```

**Acceptance Criteria**:
- [ ] Script is executable (`-rwxr-xr-x` or similar)

---

## Phase 3: Testing and Validation

### T6: Test container build and startup

**Description**: Build and test the devcontainer to ensure it works correctly.

**Requirements**: NFR-1.1, NFR-1.2, NFR-2.1, NFR-2.2, NFR-2.3

**Dependencies**: T2, T5

**Test Steps**:

1. **Build container**:
   - Open project in VS Code
   - Click "Reopen in Container" when prompted
   - Wait for build to complete

2. **Verify Python**:
   ```bash
   python --version          # Should show 3.13.1
   pyenv versions            # Should list 3.13.1 and 3.14.0
   ```

3. **Verify Poetry**:
   ```bash
   poetry --version          # Should show 2.2.1+
   poetry env info           # Should show .venv in project
   ```

4. **Verify Docker**:
   ```bash
   docker --version          # Should show Docker version
   docker ps                 # Should work without errors
   ```

5. **Verify invoke tasks**:
   ```bash
   poetry run invoke --list  # Should show all tasks
   ```

**Acceptance Criteria**:
- [ ] Container builds without errors
- [ ] Build time < 5 minutes (first build)
- [ ] Python 3.13.1 is default interpreter
- [ ] Python 3.14.0 is available via pyenv
- [ ] Poetry 2.2.1+ is installed
- [ ] Docker daemon is running
- [ ] All invoke tasks are available

---

### T7: Test all invoke tasks

**Description**: Run all invoke tasks to ensure they work in the devcontainer.

**Requirements**: FR-4.1, FR-4.2, FR-4.3, FR-4.4, FR-4.5, FR-2.2

**Dependencies**: T6

**Test Commands**:

```bash
# Run all checks
invoke project.check

# Or run individually:
invoke ruff.lint
invoke ruff.format
invoke mypy.check
invoke tests.unit
invoke tests.integration
invoke vulture.check
invoke xenon.check
invoke deptry.check
invoke pipaudit.check
invoke precommit.check
invoke trivy.check        # Uses Docker-in-Docker
invoke tests.tox          # Uses Python 3.13 + 3.14
```

**Acceptance Criteria**:
- [ ] `invoke project.check` completes successfully
- [ ] `invoke tests.unit` runs with coverage
- [ ] `invoke tests.integration` runs with coverage
- [ ] `invoke tests.tox` runs on both Python 3.13 and 3.14
- [ ] `invoke trivy.check` runs via Docker-in-Docker
- [ ] All other invoke tasks execute without errors

---

## Phase 4: Documentation Updates

### T8: Update README.md

**Description**: Add devcontainer setup instructions to README.md.

**Requirements**: FR-5.1

**Dependencies**: T7 (testing complete)

**Location**: After "Development Setup" section in README.md

**Content to add**:
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

**Acceptance Criteria**:
- [ ] README.md contains devcontainer section
- [ ] Prerequisites are clearly listed
- [ ] Step-by-step instructions are provided
- [ ] Features of devcontainer are listed

---

### T9: Update CLAUDE.md

**Description**: Add devcontainer option to CLAUDE.md development setup section.

**Requirements**: FR-5.2

**Dependencies**: T7 (testing complete)

**Location**: In "Development Setup" section of CLAUDE.md

**Content to add**:
```markdown
### DevContainer Option (Recommended)

This project supports VS Code Dev Containers for a zero-configuration development experience:

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and [VS Code Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2. Open project in VS Code
3. Click "Reopen in Container" when prompted
4. Wait for build (~5 minutes first time)

The devcontainer provides:
- Python 3.13 + 3.14 (via pyenv) for tox multi-version testing
- Poetry 2.2.1 with all dependencies pre-installed
- Docker-in-Docker for Trivy security scanning
- All VS Code extensions pre-configured
- Pre-commit hooks ready to use
```

**Acceptance Criteria**:
- [ ] CLAUDE.md contains devcontainer section
- [ ] Section explains the devcontainer benefits
- [ ] Instructions are concise

---

## Task Dependency Graph

```
T1 (Create directory)
 │
 ├──► T2 (devcontainer.json) ──► T3 (gitignore check)
 │                                      │
 └──► T4 (post-create.sh) ──► T5 (chmod +x)
                                        │
                              ┌─────────┴─────────┐
                              ▼                   ▼
                        T6 (Test build)    T7 (Test tasks)
                              │                   │
                              └─────────┬─────────┘
                                        │
                              ┌─────────┴─────────┐
                              ▼                   ▼
                        T8 (README.md)    T9 (CLAUDE.md)
```

---

## Implementation Checklist

Use this checklist to track progress:

### Phase 1: Core Configuration
- [ ] T1: Create `.devcontainer/scripts/` directory
- [ ] T2: Create `devcontainer.json` with all settings
- [ ] T3: Verify `.devcontainer` not in `.gitignore`

### Phase 2: Setup Script
- [ ] T4: Create `post-create.sh` script
- [ ] T5: Make script executable

### Phase 3: Testing
- [ ] T6: Test container build and verify tools
- [ ] T7: Test all invoke tasks pass

### Phase 4: Documentation
- [ ] T8: Update README.md with setup instructions
- [ ] T9: Update CLAUDE.md with devcontainer option

---

## Verification Commands

After implementation, run these commands to verify everything works:

```bash
# In devcontainer terminal:

# 1. Check Python versions
python --version                    # 3.13.1
pyenv versions                      # 3.13.1, 3.14.0

# 2. Check Poetry
poetry --version                    # 2.2.1+
poetry env info                     # .venv in project

# 3. Check Docker
docker --version                    # Docker installed
docker run hello-world              # Docker works

# 4. Check invoke tasks
poetry run invoke --list            # All tasks listed

# 5. Run full check
invoke project.check                # All checks pass

# 6. Run tox
invoke tests.tox                    # Tests on 3.13 + 3.14

# 7. Run Trivy
invoke trivy.check                  # Docker-in-Docker works
```

---

## Rollback Plan

If issues are encountered:

1. **Container won't build**: Check Docker Desktop is running and has sufficient resources (4GB+ RAM recommended)

2. **pyenv install fails**: The pyenv feature may need build dependencies. Check container logs for missing packages.

3. **Poetry install fails**: Delete `.venv` and `poetry.lock`, then run `poetry lock && poetry install`

4. **Extensions don't install**: Extensions install asynchronously. Reload window or install manually.

5. **Trivy fails**: Docker-in-Docker may need container restart. Try `Dev Containers: Rebuild Container`

---

## Post-Implementation

After all tasks are complete:

1. Commit all changes:
   ```bash
   git add .devcontainer/
   git commit -m "Add devcontainer support for VS Code development"
   ```

2. Test on a fresh clone to verify the complete experience

3. Consider creating a PR to merge to main branch
