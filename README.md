# lessons-learnt-from-gen-ai-career-break

<!--TOC-->

- [lessons-learnt-from-gen-ai-career-break](#lessons-learnt-from-gen-ai-career-break)
  - [Overview](#overview)
  - [Blog Part 1](#blog-part-1)
  - [Blog Part 2](#blog-part-2)
    - [Deterministic Checks](#deterministic-checks)
    - [Amazon Q Developer GitHub App Code Reviews](#amazon-q-developer-github-app-code-reviews)
    - [MD Planning Examples](#md-planning-examples)
    - [MD Review Example](#md-review-example)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
      - [1. Python 3.13+](#1-python-313)
      - [2. Poetry 2.2.1+](#2-poetry-221)
      - [3. Make](#3-make)
      - [4. Docker (Optional - for Trivy security scanning)](#4-docker-optional---for-trivy-security-scanning)
    - [Setting up your local development environment](#setting-up-your-local-development-environment)
      - [1. Clone the repository](#1-clone-the-repository)
      - [2. Run the development setup](#2-run-the-development-setup)
      - [3. Explore available tasks](#3-explore-available-tasks)
      - [4. Verify your setup](#4-verify-your-setup)
  - [Reporting Issues](#reporting-issues)

<!--TOC-->

## Overview

This repository is a public repo which supports the blog series **Lessons learnt from using Gen AI coding assistants for software development**.

## Blog Part 1

[Blog Link](https://medium.com/@julianwalls/lessons-learnt-from-using-gen-ai-coding-assistants-for-software-development-part-1-ec1353605cad)

No content added to this repo.

## Blog Part 2

[Blog Link](https://medium.com/@julianwalls/lessons-learnt-from-using-gen-ai-coding-assistants-for-software-development-part-2-6729f8cfab5d)

### Deterministic Checks

Part 2 highlights that having a good suite of deterministic checks is important when using a Gen AI coding assistant.  This repository itself demonstrates a range of deterministic checks that I tend to add to my python repositories.

- **[Ruff](https://docs.astral.sh/ruff/)** - Fast Python linter and formatter that replaces multiple tools (black, isort, flake8, pylint) with comprehensive rule coverage including security checks, code quality, and style enforcement.

- **[MyPy](https://mypy-lang.org/)** - Static type checker for Python that verifies type annotations and catches type-related errors before runtime.

- **[Pytest](https://pytest.org/)** - Modern testing framework with plugins for coverage reporting (80% required for unit tests, 70% for integration tests), mocking, and socket blocking to prevent accidental network calls.

- **[Xenon](https://github.com/rubik/xenon)** - Code complexity analyzer that measures cyclomatic complexity and enforces maximum thresholds to keep code maintainable.

- **[Vulture](https://github.com/jendrikseipp/vulture)** - Dead code detector that finds unused functions, classes, variables, and imports to keep the codebase clean.

- **[Deptry](https://deptry.com/)** - Dependency checker that identifies unused dependencies in your project and ensures all imported packages are properly declared.

- **[Pip-audit](https://pypi.org/project/pip-audit/)** - Security vulnerability scanner that checks Python dependencies against known CVEs and security advisories.

- **[Trivy](https://trivy.dev/)** - Comprehensive security scanner that detects vulnerabilities, secrets, misconfigurations, and license issues in your codebase and dependencies.

- **[Pre-commit](https://pre-commit.com/)** - Git hook framework that runs automated checks before commits, including Gitleaks for secret detection, AWS credential scanning, and prevention of direct commits to main/master branches.

All these checks are typically orchestrated in my repositories using [Invoke](https://www.pyinvoke.org/) task automation rather than traditional Makefiles. This provides a more flexible and Pythonic approach with features like hierarchical task organization, selective skipping (`--skip`), automatic safe fixes (`--apply-safe-fixes`), and unified commands.

You can run all checks with a single command (`invoke project.check`), update all dependencies at once (`invoke project.update`), or execute individual tool checks as needed. Each task includes built-in help documentation (use `invoke -h <task_name>`), and `invoke --list` displays all available tasks with descriptions, eliminating the need to read through Makefiles or documentation to discover what commands are available.

### Amazon Q Developer GitHub App Code Reviews

Part 2 mentioned that I used Amazon Q Developer GitHub App for Code Reviews extensively and that, when combined with deterministic checks, this provides a good first pass of Gen AI coding assistant changes which reduced some of the burden on a human reviewer.

This repo will have a number of closed PRs which all have [Amazon Q Developer code reviews](https://github.com/jwalls89/lessons-learnt-from-gen-ai-career-break/pulls?q=is%3Apr+is%3Aclosed).

### MD Planning Examples

Part 2, Week 2 talks about shifting left and using my first prompt to ask the Gen AI coding assistant to produce a plan first rather than jumping to an implementation.  [EXAMPLE_PLAN.md](./blog/part_2/EXAMPLE_PLAN.md) is an example from this repository when I created it and [CROSS_PLATFORM_REMEDIATION_PLAN.md] is a review that Claude Code did for me to identify cross platform issues.  It was created by [Claude Code](https://www.claude.com/product/claude-code) rather than Amazon Q Developer but gives you an idea.  In this case, I was happy with the plan and ran the plan one phase at a time, although when it came to writing the first tests, I paired with Claude Code until I was happy it knew how to implement the tests.

### MD Review Example

Although not explicitly mentioned in Part 2, I have used [Claude Code](https://www.claude.com/product/claude-code) to proofread my blogs and repository contents for spelling, grammar, consistency and coherent arguments/prose. [README_REVIEW.md](./blog/part_2/README_REVIEW.md) is an example where I had Claude review my [README](./README.md). 

## Getting Started

If you would like to use this repository.

### Prerequisites

**Note:** This repository has been developed and tested on WSL2 (Ubuntu). While it should work on other Unix-like systems (macOS, Linux), your experience may vary on untested platforms.

Before you can run this repository locally, you'll need to install the following software:

#### 1. Python 3.13+

This project requires Python 3.13.1 or later. The recommended way to install and manage Python versions is using [pyenv](https://github.com/pyenv/pyenv):

**Install pyenv:**

- **macOS/Linux:**
  ```bash
  curl https://pyenv.run | bash
  ```

- **Windows:** Use [pyenv-win](https://github.com/pyenv-win/pyenv-win)

**Install Python 3.13.1 (or later):**
```bash
pyenv install 3.13.1
```

The repository includes a `.python-version` file that will automatically activate the correct Python version when you enter the directory (if you have pyenv installed).

**Alternative:** You can also install Python directly from [python.org](https://www.python.org/downloads/), but pyenv is recommended for managing multiple Python versions.

#### 2. Poetry 2.2.1+

This project uses [Poetry](https://python-poetry.org/) for dependency management. The repository includes a `make install_poetry` command for easy installation:

```bash
make install_poetry
```

**Alternative manual installation:**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

After installation, verify the version:
```bash
poetry --version  # Should be 2.2.1 or higher
```

#### 3. Make

The Makefile provides convenient commands for setup. Make is typically pre-installed on macOS and Linux.

- **macOS:** Included with Xcode Command Line Tools (`xcode-select --install`)
- **Linux:** Usually pre-installed, or install via package manager (`apt install build-essential` or `yum install make`)
- **Windows:** Install via [chocolatey](https://chocolatey.org/) (`choco install make`) or use [WSL](https://learn.microsoft.com/en-us/windows/wsl/)

#### 4. Docker (Optional - for Trivy security scanning)

[Trivy](https://trivy.dev/) runs in a Docker container to perform comprehensive security scanning. Docker is only required if you want to run the full security checks.

- **Download:** [docker.com](https://www.docker.com/get-started)
- **Verify installation:** `docker --version`

**Note:** If Docker is not installed, you can skip Trivy checks by running:
```bash
invoke project.check --skip trivy
```

### Setting up your local development environment

Once you have all the prerequisites installed, follow these steps to set up the repository:

#### 1. Clone the repository

```bash
git clone https://github.com/jwalls89/lessons-learnt-from-gen-ai-career-break.git
cd lessons-learnt-from-gen-ai-career-break
```

#### 2. Run the development setup

The repository includes a convenient Make command that will install all dependencies and set up your development environment:

```bash
make install_dev
```

This command will:
- Install Poetry and required plugins
- Install all project dependencies (both runtime and development)
- Set up pre-commit hooks
- Activate the Poetry virtual environment shell

#### 3. Explore available tasks

This project uses [Invoke](https://www.pyinvoke.org/) for task automation. To see all available commands, run:

```bash
invoke --list
```

**Available tasks:**

```
Available tasks:

  deptry.check        Run deptry to check for unused dependencies.
  mypy.check          Run mypy to check for type errors.
  pipaudit.check      Run pip-audit to check for vulnerable dependencies.
  poetry.update       Update all poetry dependencies.
  precommit.check     Run pre-commit checks.
  precommit.update    Update pre-commit hooks to latest versions.
  project.check       Run all project checks.
  project.update      Update all dependencies and pre-commit hooks.
  ruff.format         Run ruff to format code.
  ruff.lint           Run ruff to check for code style issues.
  tests.integration   Run integration tests using pytest.
  tests.tox           Run multi-version testing using tox.
  tests.unit          Run unit tests using pytest.
  trivy.check         Run trivy security scanner using Docker to scan the
                      filesystem for vulnerabilities and security issues.
  vulture.check       Run vulture to check for unused code.
  xenon.check         Run xenon to check for code complexity.
```

#### 4. Verify your setup

Run all checks to ensure everything is working correctly:

```bash
invoke project.check
```

This will run all deterministic checks including linting, type checking, tests, and security scans.

**Note:** If you don't have Docker installed, skip the Trivy check:
```bash
invoke project.check --skip trivy
```

For more details on individual commands and development workflows, see the [CLAUDE.md](CLAUDE.md) file.

## Reporting Issues

If you find any issues with this repository, please [raise an issue](https://github.com/jwalls89/lessons-learnt-from-gen-ai-career-break/issues) on GitHub. Feedback and suggestions are welcome!
