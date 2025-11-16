"""Actionlint tasks for checking GitHub Actions workflows."""

from invoke import task
from invoke.collection import Collection
from invoke.context import Context


@task
def check(context: Context) -> None:
    """Run actionlint to check GitHub Actions workflows."""
    context.run("poetry run actionlint", echo=True)


collection = Collection("actionlint")
collection.add_task(check, "check")
