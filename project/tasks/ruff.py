"""Ruff linting and formatting tasks."""

from invoke import task
from invoke.collection import Collection
from invoke.context import Context


@task
def lint(context: Context, *, apply_safe_fixes: bool = False, apply_unsafe_fixes: bool = False) -> None:
    """Run ruff to check for code style issues."""
    if apply_safe_fixes:
        context.run("poetry run ruff check . --fix ", echo=True)
    elif apply_unsafe_fixes:
        context.run("poetry run ruff check . --unsafe-fixes", echo=True)
    else:
        context.run("poetry run ruff check . --no-fix", echo=True)


@task
def format(context: Context, *, apply_safe_fixes: bool = False) -> None:  # noqa: A001
    """Run ruff to format code."""
    if apply_safe_fixes:
        context.run("poetry run ruff format . --no-preview", echo=True)
    else:
        context.run("poetry run ruff format . --check", echo=True)


collection = Collection("ruff")
collection.add_task(lint)
collection.add_task(format)
