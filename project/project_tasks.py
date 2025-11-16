"""Project-level tasks for updating dependencies and running all checks."""

from invoke import task
from invoke.collection import Collection
from invoke.context import Context

from project import deptry, mypy, pipaudit, precommit, ruff, testing, vulture, xenon


@task
def update(context: Context) -> None:
    """Update all dependencies and pre-commit hooks."""
    context.run("poetry update", echo=True)
    context.run("poetry run pre-commit autoupdate", echo=True)


@task
def check(context: Context, *, apply_safe_fixes: bool = False, apply_unsafe_fixes: bool = False) -> None:
    """Run all project checks."""
    # actionlint.check(context) # noqa: ERA001 Needs actionlint adding to github
    deptry.check(context)
    mypy.check(context)
    precommit.check(context)
    ruff.format(context, apply_safe_fixes=apply_safe_fixes)
    ruff.lint(context, apply_safe_fixes=apply_safe_fixes, apply_unsafe_fixes=apply_unsafe_fixes)
    pipaudit.check(context)
    vulture.check(context)
    xenon.check(context)
    testing.unit(context)
    testing.integration(context)


collection = Collection("project")
collection.add_task(update)
collection.add_task(check)
