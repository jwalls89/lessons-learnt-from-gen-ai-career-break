# Devcontainer Support - Requirements

## Overview

This document defines the requirements for adding devcontainer support to the lessons-learnt-from-gen-ai-career-break project.

## Stakeholders

| Stakeholder | Needs |
|-------------|-------|
| Solo developer | Consistent environment across machines |
| New team members | Quick onboarding without manual setup |
| Open source contributors | Low barrier to entry |
| Blog readers/learners | Easy replication of development setup |

## Functional Requirements

### FR-1: Development Environment

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1.1 | Container provides Python 3.13.1 as the primary interpreter | Must |
| FR-1.2 | Container provides Python 3.14.0 for tox multi-version testing | Must |
| FR-1.3 | Poetry 2.2.1+ is installed and configured | Must |
| FR-1.4 | poetry-plugin-export is available | Must |
| FR-1.5 | All development dependencies install successfully via `poetry install` | Must |
| FR-1.6 | Pre-commit hooks install and run correctly | Must |

### FR-2: Docker Support

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-2.1 | Docker daemon is available inside the container (Docker-in-Docker) | Must |
| FR-2.2 | `invoke trivy.check` executes successfully | Must |
| FR-2.3 | Docker state is isolated from host system | Should |

### FR-3: VS Code Integration

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-3.1 | VS Code automatically prompts to reopen in container | Must |
| FR-3.2 | Python extensions auto-install and configure | Must |
| FR-3.3 | Ruff extension integrates with project settings | Must |
| FR-3.4 | All specified extensions install automatically | Should |

### FR-4: Task Execution

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-4.1 | `invoke project.check` runs all checks successfully | Must |
| FR-4.2 | `invoke tests.unit` executes with coverage | Must |
| FR-4.3 | `invoke tests.integration` executes with coverage | Must |
| FR-4.4 | `invoke tests.tox` runs multi-version tests | Must |
| FR-4.5 | All invoke tasks from `invoke --list` are functional | Must |

### FR-5: Documentation

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-5.1 | README.md includes devcontainer setup instructions | Must |
| FR-5.2 | CLAUDE.md is updated to reflect devcontainer option | Should |

## Non-Functional Requirements

### NFR-1: Performance

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1.1 | Initial container build time | < 5 minutes |
| NFR-1.2 | Container startup time (after build) | < 30 seconds |
| NFR-1.3 | `poetry install` completion time | < 2 minutes |

### NFR-2: Compatibility

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-2.1 | Works on Docker Desktop for Windows | Must |
| NFR-2.2 | Works on Docker Desktop for macOS | Must |
| NFR-2.3 | Works on Docker CE/EE on Linux | Must |
| NFR-2.4 | Works with VS Code Dev Containers extension | Must |

### NFR-3: Maintainability

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-3.1 | Uses Microsoft DevContainers base images | Must |
| NFR-3.2 | Uses DevContainer features over custom scripts | Should |
| NFR-3.3 | Minimal custom Dockerfile (if any) | Should |

## User Stories

### US-1: New Developer Onboarding

**As a** new developer joining the project
**I want to** open the repository in VS Code and have a working environment automatically
**So that** I can start contributing immediately without manual setup

**Acceptance Criteria**:
- [ ] Clone repository and open in VS Code
- [ ] VS Code prompts to reopen in container
- [ ] Container builds successfully on first attempt
- [ ] All extensions are installed and functional
- [ ] `invoke --list` shows all available tasks
- [ ] `invoke project.check` passes (or shows only expected warnings)
- [ ] Can create a branch, make changes, and commit

### US-2: Run Full Test Suite

**As a** developer
**I want to** run the complete test suite including multi-version testing
**So that** I can verify my changes work across Python versions before pushing

**Acceptance Criteria**:
- [ ] `invoke tests.unit` runs with coverage report
- [ ] `invoke tests.integration` runs with coverage report
- [ ] `invoke tests.tox` tests against Python 3.13 and 3.14
- [ ] Coverage reports are generated in `.quality/pytest-cov/`

### US-3: Run Security Checks

**As a** developer
**I want to** run all security checks including Trivy
**So that** I can identify vulnerabilities before committing

**Acceptance Criteria**:
- [ ] `invoke pipaudit.check` runs successfully
- [ ] `invoke trivy.check` runs successfully (uses Docker-in-Docker)
- [ ] Pre-commit hooks run on commit (including gitleaks)

### US-4: Code Quality Workflow

**As a** developer
**I want to** see linting errors and type issues in VS Code as I code
**So that** I can fix issues immediately rather than waiting for CI

**Acceptance Criteria**:
- [ ] Ruff shows linting errors inline in editor
- [ ] Pylance shows type errors inline in editor
- [ ] Format on save works with Ruff
- [ ] `invoke ruff.lint --apply-safe-fixes` auto-fixes issues

### US-5: Blog Reader Setup

**As a** reader of the lessons-learnt blog
**I want to** quickly set up the exact development environment used in the blog
**So that** I can follow along with examples and experiment

**Acceptance Criteria**:
- [ ] README clearly explains devcontainer prerequisites (Docker, VS Code)
- [ ] README provides step-by-step instructions to open in container
- [ ] Container works without any additional configuration
- [ ] All tools mentioned in blog posts are available

## VS Code Extensions

The following extensions will be pre-installed:

### Python Development (5)
| Extension ID | Purpose |
|-------------|---------|
| `ms-python.python` | Core Python language support |
| `ms-python.vscode-pylance` | Python language server |
| `ms-python.debugpy` | Python debugging |
| `ms-python.vscode-python-envs` | Python environment management |
| `charliermarsh.ruff` | Linting and formatting |

### Project Utilities (3)
| Extension ID | Purpose |
|-------------|---------|
| `ms-vscode.makefile-tools` | Makefile support |
| `redhat.vscode-yaml` | YAML validation |
| `github.vscode-github-actions` | GitHub Actions workflow editing |

### AI Assistants (4)
| Extension ID | Purpose |
|-------------|---------|
| `anthropic.claude-code` | Claude Code integration |
| `github.copilot` | GitHub Copilot |
| `github.copilot-chat` | Copilot Chat |
| `amazonwebservices.amazon-q-vscode` | Amazon Q |

### AWS Development (2)
| Extension ID | Purpose |
|-------------|---------|
| `amazonwebservices.aws-toolkit-vscode` | AWS Toolkit |
| `boto3typed.boto3-ide` | Boto3 type hints |

### Documentation (1)
| Extension ID | Purpose |
|-------------|---------|
| `vstirbu.vscode-mermaid-preview` | Mermaid diagram preview |

## Configuration Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Base image approach | Hybrid (Microsoft + features) | Balance of simplicity and maintainability |
| Docker support | Docker-in-Docker | Enables Trivy, isolated from host |
| Python versions | 3.13 + 3.14 | Matches .python-version and tox config |
| Shell | Bash | Simple, familiar, smaller image |
| GPG signing | Not supported | Not required by project |
| Codespaces | Not required | Local development focus |

## Out of Scope

- GitHub Codespaces optimization
- GPG commit signing support
- Custom shell configuration (zsh/oh-my-zsh)
- Windows container support
- Remote Docker host support

## Dependencies

- Docker Desktop (Windows/macOS) or Docker CE/EE (Linux)
- VS Code with Dev Containers extension (`ms-vscode-remote.remote-containers`)
- Internet connection for initial image pull and extension installation

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Python 3.14 not available in base image | Cannot run tox multi-version | Use pyenv or deadsnakes PPA in postCreateCommand |
| Docker-in-Docker performance | Slower Trivy scans | Acceptable trade-off for isolation |
| Large image size | Longer initial download | Use minimal features, document expected size |
| Extension compatibility | Some extensions may not work in container | Test all extensions during implementation |

## Success Criteria

1. New developer can go from `git clone` to running `invoke project.check` in under 10 minutes
2. All CI checks that pass locally also pass in devcontainer
3. Tox multi-version testing works in devcontainer
4. Trivy security scanning works via Docker-in-Docker
5. README provides clear setup instructions for devcontainer
