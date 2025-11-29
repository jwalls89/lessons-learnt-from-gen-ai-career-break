# Plan: Devcontainer Check GitHub Action

## Goal

Add a GitHub Action that verifies the devcontainer works correctly, balancing thoroughness with CI speed/cost.

## Design Principles

- **Parity between local and CI**: Same verification steps, different entry points
  - Local: `invoke devcontainer.check` (developer already has Poetry)
  - CI: `npx @devcontainers/cli` directly (avoid installing Python/Poetry just to run the check)
- **Path-based triggering**: Only run full check when relevant files change
- **Weekly external drift check**: Catch base image/dependency changes

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Quick check (CI) | `npx @devcontainers/cli build` | Fast (~1-2 min), catches Dockerfile issues |
| Full check (CI) | `devcontainers/ci` action with `invoke project.check` | Catches missing commands, broken tasks |
| Local check | `invoke devcontainer.check` with flags | Same steps, familiar interface for developers |
| Triggering | Path-based | Only run full check when relevant files change |
| External drift | Weekly scheduled run | Catches base image/dependency drift without daily cost |
| Caching | None | Simplicity over speed; avoid storage costs and staleness |
| Reusability | Composite action | Follows existing pattern in `.github/actions/` |

## Command Reference

### Local (via invoke)

| Command | What it does |
|---------|--------------|
| `invoke devcontainer.check --build-only` | Build image only (quick) |
| `invoke devcontainer.check` | Build + up + `invoke --list` (standard) |
| `invoke devcontainer.check --run-project-check` | Build + up + `invoke project.check` (full) |

### CI (via npx / devcontainers/ci)

| Step | Command |
|------|---------|
| Quick check | `npx @devcontainers/cli build --workspace-folder .` |
| Full check | `devcontainers/ci` action with `runCmd: poetry run invoke project.check` |

## Path Triggers

Files that trigger **full** devcontainer verification:
- `.devcontainer/**` - Dockerfile, devcontainer.json, scripts
- `pyproject.toml` - Dependencies
- `poetry.lock` - Locked dependencies
- `project/**` - Invoke task definitions
- `tasks.py` - Task collection entrypoint

All other changes get **quick** build-only check.

## Implementation Tasks

### Task 1: Extend Devcontainer Task with Flags

Update `project/tasks/devcontainer.py`:

```python
@task
def check(context: Context, build_only: bool = False, run_project_check: bool = False) -> None:
    """Verify the devcontainer builds and runs correctly in headless mode.

    Args:
        build_only: Only build the image, skip up and exec (fast check)
        run_project_check: Run 'invoke project.check' inside container instead of 'invoke --list'
    """
    workspace_path = get_current_working_directory()

    context.run("docker info", hide=True)

    context.run(
        f"npx @devcontainers/cli build --workspace-folder {workspace_path}",
        echo=True,
    )

    if build_only:
        return

    context.run(
        f"npx @devcontainers/cli up --workspace-folder {workspace_path}",
        echo=True,
    )

    verify_cmd = "poetry run invoke project.check" if run_project_check else "poetry run invoke --list"
    context.run(
        f"npx @devcontainers/cli exec --workspace-folder {workspace_path} {verify_cmd}",
        echo=True,
    )


collection = Collection("devcontainer")
collection.add_task(check)
```

### Task 2: Create Composite Action

Create `.github/actions/devcontainer-check/action.yml`:

```yaml
name: 'Devcontainer Check'
description: 'Build and verify the devcontainer works correctly'

inputs:
  full-check:
    description: 'Run full verification (true) or quick build only (false)'
    required: false
    default: 'false'

runs:
  using: 'composite'
  steps:
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: 'lts/*'

    - name: Quick build check
      if: inputs.full-check == 'false'
      shell: bash
      run: npx @devcontainers/cli build --workspace-folder .

    - name: Full devcontainer verification
      if: inputs.full-check == 'true'
      uses: devcontainers/ci@v0.3
      with:
        runCmd: poetry run invoke project.check
```

### Task 3: Update PR Workflow

Update `.github/workflows/pr.yml` to add devcontainer check job:

```yaml
devcontainer-check:
  needs: check-fork
  runs-on: ubuntu-latest
  steps:
    - name: Checkout
      uses: actions/checkout@v5

    - name: Check for relevant changes
      id: changes
      uses: dorny/paths-filter@v3
      with:
        filters: |
          full-check:
            - '.devcontainer/**'
            - 'pyproject.toml'
            - 'poetry.lock'
            - 'project/**'
            - 'tasks.py'

    - name: Run devcontainer check
      uses: ./.github/actions/devcontainer-check
      with:
        full-check: ${{ steps.changes.outputs.full-check }}
```

### Task 4: Update Main Workflow

Update `.github/workflows/main.yml` to add devcontainer check job (always full check on main):

```yaml
devcontainer-check:
  runs-on: ubuntu-latest
  steps:
    - name: Checkout
      uses: actions/checkout@v5

    - name: Run devcontainer check
      uses: ./.github/actions/devcontainer-check
      with:
        full-check: 'true'
```

### Task 5: Create Weekly Scheduled Workflow

Create `.github/workflows/devcontainer-weekly.yml`:

```yaml
name: Weekly Devcontainer Check

on:
  schedule:
    - cron: '0 6 * * 0'  # Sunday at 6am UTC
  workflow_dispatch:      # Manual trigger

jobs:
  devcontainer-check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v5

      - name: Run full devcontainer check
        uses: ./.github/actions/devcontainer-check
        with:
          full-check: 'true'
```

### Task 6: Update CLAUDE.md

Add documentation for:
- New `--build-only` and `--run-project-check` flags
- Weekly devcontainer workflow
- Devcontainer check composite action

## Verification Matrix

| Trigger | CI Command | Local Equivalent | Catches |
|---------|------------|------------------|---------|
| PR (no relevant changes) | `npx @devcontainers/cli build` | `invoke devcontainer.check --build-only` | Dockerfile syntax, base image pull |
| PR (relevant files changed) | `devcontainers/ci` + `invoke project.check` | `invoke devcontainer.check --run-project-check` | Above + post-create, missing packages, broken tasks |
| Push to main | `devcontainers/ci` + `invoke project.check` | `invoke devcontainer.check --run-project-check` | Everything |
| Weekly schedule | `devcontainers/ci` + `invoke project.check` | `invoke devcontainer.check --run-project-check` | External drift (base image, apt, npm) |

## Files to Create/Modify

| File | Action |
|------|--------|
| `project/tasks/devcontainer.py` | Modify (add flags) |
| `.github/actions/devcontainer-check/action.yml` | Create |
| `.github/workflows/pr.yml` | Modify |
| `.github/workflows/main.yml` | Modify |
| `.github/workflows/devcontainer-weekly.yml` | Create |
| `CLAUDE.md` | Modify |

## Open Questions

None - design approved by user.

## Rollback Plan

If issues arise, simply remove the devcontainer-check job from workflows. Existing CI continues to work independently. The invoke task flags are backwards-compatible (default behaviour unchanged).
