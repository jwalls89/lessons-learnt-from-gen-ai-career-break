# Devcontainer Support - Discovery

## Problem Statement

The project currently requires manual setup of Python 3.13+, Poetry 2.2.1+, and various development tools (pyenv, pre-commit, etc.). This creates several challenges:

1. **Slow onboarding** - New developers or blog readers must manually install pyenv, Poetry, and configure their environment
2. **Environment inconsistency** - Different local environments can lead to "works on my machine" issues
3. **Local environment pollution** - Installing Python versions, Poetry, and tools globally affects other projects
4. **Cross-platform friction** - Windows users have additional setup complexity (WSL recommended)

## Business Value

| Stakeholder | Benefit |
|-------------|---------|
| Solo developer | Consistent environment across machines; quick project startup on new devices |
| New team members | Zero-to-productive in minutes instead of hours |
| Open source contributors | Lower barrier to entry; immediate contribution capability |
| Blog readers/learners | Easy replication of exact development setup from lessons-learnt series |

## Current Development Environment

### Tooling Requirements
- **Python**: 3.13.1 (primary), 3.14.0 (secondary/testing)
- **Package Manager**: Poetry 2.2.1+ with `poetry-plugin-export`
- **Task Runner**: invoke
- **Code Quality**: ruff, mypy, vulture, xenon, deptry
- **Testing**: pytest (with socket, mock, order, cov plugins), tox
- **Security**: pre-commit (gitleaks), pip-audit, trivy (Docker-based)
- **Docs/Format**: Line length 120, double quotes, 4-space indent

### CI/CD Matrix
- **Platforms**: ubuntu-latest, macos-latest (Windows removed)
- **Python Versions**: 3.13 (primary), 3.14 (testing)

### Docker Dependency
Trivy security scanning requires Docker. Currently optional - users can skip with `--skip trivy.check`.

## Research: Existing Solutions

### 1. Microsoft DevContainers Base Images
**Source**: [Microsoft DevContainers](https://github.com/microsoft/vscode-dev-containers)

- Pre-built images: `mcr.microsoft.com/devcontainers/python:3.13-bullseye`
- Feature system for modular tool installation
- Well-maintained, widely adopted
- Integrated VS Code extension support

**Pros**: Fast startup, minimal configuration, automatic updates
**Cons**: Less control over base OS, may include unnecessary tools

### 2. Custom Dockerfile Approach
**Source**: [Python Poetry Discussion](https://github.com/orgs/python-poetry/discussions/1879)

- Build from `python:3.13-slim-bookworm`
- Full control over installed packages
- Can optimize for size

**Pros**: Complete control, minimal image size
**Cons**: More maintenance, slower builds, reinventing solved problems

### 3. Hybrid Approach (Recommended)
**Source**: [NHS Digital Repository Template](https://github.com/NHSDigital/repository-template), [DevContainers Discussion #41](https://github.com/orgs/devcontainers/discussions/41)

- Microsoft base image (Ubuntu or Python-specific)
- DevContainer features for tooling (Docker-in-Docker, Python, etc.)
- `postCreateCommand` for project-specific setup

**Example from NHS Digital**:
- Ubuntu base with Docker-in-Docker feature
- Python feature for version management
- pre-commit installed via pipx
- GPG mount for commit signing

**Pros**: Best of both worlds - managed base with customization
**Cons**: Dependency on Microsoft feature ecosystem

### 4. Reference Implementations

**[a5chin/python-poetry](https://github.com/a5chin/python-poetry)**:
- Poetry + pyenv + Ruff in devcontainer
- `virtualenvs.create false` approach
- Comprehensive VS Code extension list

**Key Best Practices Identified**:
1. Use `postStartCommand` or `postAttachCommand` for `poetry install` (not baked into image)
2. Set `virtualenvs.in-project: true` for caching
3. Use devcontainer features over manual installation
4. Include essential VS Code extensions in configuration

## Approach Decision

### Recommended: Hybrid with Microsoft Base + Features

**Configuration Strategy**:
```
Base: mcr.microsoft.com/devcontainers/python:3.13-bookworm
      (or ubuntu:noble with Python feature for Python 3.14 flexibility)

Features:
- Docker-in-Docker (for Trivy support)
- Python (if using Ubuntu base)
- Common utilities

postCreateCommand: Install Poetry, run poetry install, pre-commit install
```

### Docker-in-Docker Complexity

Docker-in-Docker is supported via the `ghcr.io/devcontainers/features/docker-in-docker` feature. This enables:
- Running `docker` commands inside the container
- Trivy scanning via `aquasec/trivy` image

**Complexity Notes**:
1. **Socket access**: The feature handles Docker socket mounting/creation
2. **Performance**: Nested Docker can be slower than host Docker
3. **Storage**: Docker images pulled inside container don't persist by default
4. **Alternative**: Docker-outside-of-Docker mounts host socket (simpler but shares Docker state)

The feature approach abstracts most complexity - users don't need to configure Docker manually.

### Why Not Custom Dockerfile?

1. This project's tooling (Poetry, pyenv-style Python, pre-commit) is well-supported by features
2. Maintenance burden of Dockerfile updates for security patches
3. No unique requirements that features can't handle
4. Blog readers benefit from standardized, documented approach

### Why Not Docker-outside-of-Docker?

Docker-in-Docker is recommended because:
1. Isolation - container's Docker state doesn't affect host
2. Portability - works in Codespaces and remote Docker hosts
3. The NHS Digital template uses this approach successfully

## Open Questions

1. **Python 3.14 Support**: Microsoft images may not have 3.14 yet. May need Ubuntu base with pyenv feature.
2. **VS Code Extensions**: Which extensions are essential vs. nice-to-have?
3. **Tox Multi-version Testing**: How to provide multiple Python versions in devcontainer?
4. **GPG Signing**: Should we support commit signing like NHS template?

## Decision Summary

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| Base Image | Microsoft Python 3.13 or Ubuntu with Python feature | Best balance of simplicity and flexibility |
| Docker Support | Docker-in-Docker feature | Enables Trivy, isolated from host |
| Poetry | Installed in postCreateCommand | Allows version pinning, follows best practices |
| VS Code Extensions | Python, Pylance, Ruff, GitLens | Matches current project tooling |
| Approach | Hybrid (base + features) | Maintainable, documented, portable |

## Next Steps

1. Define detailed requirements (Phase 1)
2. Design devcontainer.json structure (Phase 2)
3. Create implementation tasks (Phase 3)

---

## Sources

- [VS Code DevContainers Documentation](https://code.visualstudio.com/docs/devcontainers/containers)
- [DevContainers Poetry Best Practices Discussion](https://github.com/orgs/devcontainers/discussions/41)
- [NHS Digital Repository Template](https://github.com/NHSDigital/repository-template)
- [a5chin/python-poetry DevContainer Example](https://github.com/a5chin/python-poetry)
- [Python Poetry Docker Best Practices](https://github.com/orgs/python-poetry/discussions/1879)
- [Microsoft Python DevContainer Image](https://github.com/microsoft/vscode-dev-containers/blob/main/containers/python-3/README.md)
