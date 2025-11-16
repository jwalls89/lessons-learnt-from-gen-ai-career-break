"""Pre-commit tasks for running hooks."""

from invoke import task
from invoke.collection import Collection
from invoke.context import Context


@task
def check(context: Context, *, apply_safe_fixes: bool = False) -> None:
    """Run pre-commit checks."""
    if apply_safe_fixes:
        context.run("poetry run pre-commit run end-of-file-fixer --all-files", echo=True, warn=True)
        context.run("poetry run pre-commit run md-toc --all-files", echo=True, warn=True)
    context.run("poetry run pre-commit run --all-files", echo=True)


@task
def update(context: Context) -> None:
    """Update pre-commit hooks to latest versions."""
    context.run("poetry run pre-commit autoupdate", echo=True)


collection = Collection("precommit")
collection.add_task(check, "check")
collection.add_task(update, "update")
