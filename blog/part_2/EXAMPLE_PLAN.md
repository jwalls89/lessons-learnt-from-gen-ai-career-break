# Task Module Refactoring Plan

## Overview

Refactor the monolithic `tasks.py` file into a modular structure with separate modules for each tool under a new `project/` directory.

## Current State

- **Single file**: `tasks.py` (~185 lines)
- **10 task collections**: actionlint, deptry, mypy, precommit, ruff, pipaudit, tests, vulture, xenon, project
- **15 total tasks** across all collections
- **Pattern**: Most tasks follow a simple "run command" pattern with some having additional complexity

## Proposed Structure

```
project/
├── __init__.py              # Package initialization
├── actionlint.py            # Actionlint tasks
├── deptry.py                # Deptry tasks
├── mypy.py                  # MyPy tasks
├── precommit.py             # Pre-commit tasks
├── ruff.py                  # Ruff tasks (lint + format)
├── pipaudit.py              # Pip-audit tasks
├── testing.py               # Test tasks (unit, integration, tox)
├── vulture.py               # Vulture tasks
├── xenon.py                 # Xenon tasks
└── project_tasks.py         # Project-level tasks (update, check)

tasks.py                     # Main entry point (simplified to imports)
```

## Design Principles

### Module Organization
- **One module per tool**: Each tool gets its own dedicated module file
- **Consistent naming**: Module names match the invoke collection names (e.g., `ruff.py` → `invoke ruff.lint`)
- **Standard exports**: Each module exports a `collection` object that tasks.py imports

### Code Patterns

#### Simple Module Pattern (for tools with single "check" task)
```python
"""Tool description."""
from invoke import task
from invoke.collection import Collection
from invoke.context import Context

@task
def check(context: Context) -> None:
    """Run tool to check for issues."""
    context.run("poetry run tool-command", echo=True)

collection = Collection("tool-name")
collection.add_task(check)
```

**Applies to**: actionlint, deptry, mypy, precommit, pipaudit, vulture, xenon

#### Complex Module Pattern (for tools with multiple tasks or parameters)
```python
"""Tool description."""
from invoke import task
from invoke.collection import Collection
from invoke.context import Context

@task
def task_one(context: Context, *, param: bool = False) -> None:
    """First task."""
    # Implementation

@task
def task_two(context: Context) -> None:
    """Second task."""
    # Implementation

collection = Collection("tool-name")
collection.add_task(task_one, "name")
collection.add_task(task_two, "name")
```

**Applies to**: ruff (lint, format), testing (unit, integration, tox), project_tasks (update, check)

## Module Details

### Simple Modules

#### actionlint.py
- **Tasks**: check
- **Command**: `poetry run actionlint`
- **Notes**: Currently commented out in project.check (needs actionlint in GitHub)

#### deptry.py
- **Tasks**: check
- **Command**: `poetry run deptry .`

#### mypy.py
- **Tasks**: check
- **Command**: `poetry run mypy .`

#### precommit.py
- **Tasks**: check
- **Command**: `poetry run pre-commit run --all-files`

#### vulture.py
- **Tasks**: check
- **Command**: `poetry run vulture . vulture_whitelist`

#### xenon.py
- **Tasks**: check
- **Command**: `poetry run xenon --max-absolute B --max-modules A --max-average A .`

### Complex Modules

#### ruff.py
- **Tasks**: lint, format
- **Parameters**:
  - `apply_safe_fixes` (bool): Apply safe fixes/formatting
  - `apply_unsafe_fixes` (bool): Apply unsafe fixes (lint only)
- **Commands**:
  - Lint: `ruff check .` with `--fix`, `--unsafe-fixes`, or `--no-fix`
  - Format: `ruff format .` with or without `--check`

#### pipaudit.py
- **Tasks**: check
- **Complexity**: Multi-step process
  1. Create `.quality/pipaudit/` directory
  2. Export main requirements to `.quality/pipaudit/requirements-main.txt`
  3. Export dev requirements to `.quality/pipaudit/requirements-dev.txt`
  4. Run pip-audit on both files

#### testing.py
- **Tasks**: unit, integration, tox
- **Commands**:
  - Unit: `pytest tests/unit/` with coverage config
  - Integration: `pytest tests/integration/` with coverage config
  - Tox: `poetry run tox`

#### project_tasks.py
- **Tasks**: update, check
- **Complexity**:
  - `update`: Runs two commands (poetry update, pre-commit autoupdate)
  - `check`: Orchestrates all other check tasks with parameter forwarding
- **Parameters**:
  - `apply_safe_fixes` (bool): Passed to ruff tasks
  - `apply_unsafe_fixes` (bool): Passed to ruff.lint
- **Notes**: Imports functions from other modules

## Updated tasks.py

```python
"""Invoke task collections for project development tasks."""

from invoke.collection import Collection

# Import all task modules
from project import (
    actionlint,
    deptry,
    mypy,
    pipaudit,
    precommit,
    project_tasks,
    ruff,
    testing,
    vulture,
    xenon,
)

# Create root namespace
ns = Collection()

# Register all collections
ns.add_collection(actionlint.collection)
ns.add_collection(deptry.collection)
ns.add_collection(mypy.collection)
ns.add_collection(pipaudit.collection)
ns.add_collection(precommit.collection)
ns.add_collection(project_tasks.collection)
ns.add_collection(ruff.collection)
ns.add_collection(testing.collection)
ns.add_collection(vulture.collection)
ns.add_collection(xenon.collection)
```

## Migration Steps

### Phase 1: Setup (10 min)
1. ✅ Create plan document for review
2. Create `project/` directory
3. Create `project/__init__.py` (empty or with package docstring)

### Phase 2: Migrate Simple Modules (30 min)
4. Create and test `project/actionlint.py`
5. Create and test `project/deptry.py`
6. Create and test `project/mypy.py`
7. Create and test `project/precommit.py`
8. Create and test `project/vulture.py`
9. Create and test `project/xenon.py`

**Testing approach**: After each module, update tasks.py imports and run `invoke --list` to verify

### Phase 3: Migrate Complex Modules (45 min)
10. Create and test `project/ruff.py`
11. Create and test `project/pipaudit.py`
12. Create and test `project/testing.py`
13. Create and test `project/project_tasks.py` (requires imports from other modules)

**Testing approach**: Test individual tasks (e.g., `invoke ruff.lint`, `invoke tests.unit`)

### Phase 4: Integration (30 min)
14. Update `tasks.py` with all imports
15. Run `invoke --list` to verify all tasks registered
16. Run `invoke project.check` to ensure end-to-end functionality
17. Run individual tasks to spot-check: `invoke ruff.lint`, `invoke mypy.check`, etc.

### Phase 5: Documentation & Cleanup (30 min)
18. Update `CLAUDE.md` to reflect new structure
19. Update project structure diagram
20. Add notes about module organization
21. Consider updating `.pre-commit-config.yaml` if needed (currently excludes tasks.py from some checks)
22. Run final `invoke project.check --apply-safe-fixes`
23. Commit changes

**Total estimated time**: ~2.4 hours

## Benefits

### Maintainability
- **Smaller files**: Each module 15-30 lines vs. 185-line monolith
- **Single responsibility**: Each module focuses on one tool
- **Easier to understand**: No need to scroll through entire file to find a task

### Discoverability
- **Predictable locations**: Know exactly where to find task definitions
- **Clear ownership**: One file per tool makes it obvious where changes go
- **IDE-friendly**: Better autocomplete and navigation

### Testability
- **Unit testable**: Each module can have its own test file
- **Isolated changes**: Modifications to one tool don't risk breaking others
- **Easier mocking**: Can mock individual modules in tests

### Scalability
- **Easy to extend**: Add new tools by creating new module files
- **Parallel development**: Multiple people can work on different modules
- **Reduced merge conflicts**: Changes spread across files instead of one file

### Clarity
- **Self-contained modules**: Each module has all logic inline, no indirection
- **Consistent patterns**: Clear templates for new modules
- **Explicit over implicit**: Commands written out in full for easy understanding

## Open Questions

1. **Naming**: Should test module be `testing.py` or `pytest.py`?
   - Recommendation: `testing.py` (more general, matches "tests" collection name)

2. **Naming**: Should project tasks be `project_tasks.py` or something else?
   - Recommendation: `project_tasks.py` (avoids confusion with folder name)

3. **Testing**: Should we add tests for the task modules?
   - Recommendation: Out of scope for this refactoring, but good future enhancement

## Risks & Mitigation

### Risk: Breaking existing workflows
- **Mitigation**: Keep tasks.py as entry point, all `invoke` commands stay the same
- **Testing**: Run full `invoke project.check` before and after migration

### Risk: Import errors or circular dependencies
- **Mitigation**: Follow consistent pattern (modules export `collection`, tasks.py imports)
- **Testing**: Run `invoke --list` frequently during migration

### Risk: Missing task parameters or flags
- **Mitigation**: Copy exact function signatures from original tasks.py
- **Testing**: Spot-check tasks with parameters (e.g., `invoke ruff.lint --apply-safe-fixes`)

### Risk: Breaking pre-commit or CI/CD
- **Mitigation**: Test locally before committing, review `.pre-commit-config.yaml`
- **Testing**: Run `invoke precommit.check` before final commit

## Success Criteria

- ✅ All `invoke` commands work exactly as before
- ✅ `invoke --list` shows all 15 tasks across 10 collections
- ✅ `invoke project.check` passes completely
- ✅ Code passes all quality checks (ruff, mypy, etc.)
- ✅ CLAUDE.md updated with new structure
- ✅ Each module file is self-contained and well-documented
- ✅ All commands written explicitly inline for clarity

## Future Enhancements (Out of Scope)

- Add unit tests for task modules
- Consider adding task decorators for common behavior (if clear patterns emerge)
- Explore task dependencies and prerequisites
- Add task-level configuration file support
