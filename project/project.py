"""Project-level tasks for updating dependencies and running all checks."""

from invoke import task
from invoke.collection import Collection
from invoke.context import Context

from project import deptry, mypy, pipaudit, poetry, precommit, ruff, testing, vulture, xenon


@task
def update(context: Context) -> None:
    """Update all dependencies and pre-commit hooks."""
    poetry.update(context)
    precommit.update(context)


@task
def check(context: Context, *, apply_safe_fixes: bool = False, apply_unsafe_fixes: bool = False) -> None:
    """Run all project checks."""
    # actionlint.check(context) # noqa: ERA001 Needs actionlint adding to github   
    precommit.check(context)
    ruff.format(context, apply_safe_fixes=apply_safe_fixes)
    ruff.lint(context, apply_safe_fixes=apply_safe_fixes, apply_unsafe_fixes=apply_unsafe_fixes)
    mypy.check(context)
    vulture.check(context)
    xenon.check(context)
    testing.unit(context)
    testing.integration(context)
    pipaudit.check(context)
    deptry.check(context)


collection = Collection("project")
collection.add_task(update)
collection.add_task(check)
