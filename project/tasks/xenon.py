"""Xenon tasks for checking code complexity."""

from invoke import task
from invoke.collection import Collection
from invoke.context import Context


@task
def check(context: Context) -> None:
    """Run xenon to check for code complexity."""
    context.run("poetry run xenon --max-absolute B --max-modules A --max-average A .", echo=True)


collection = Collection("xenon")
collection.add_task(check, "check")
