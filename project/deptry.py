"""Deptry tasks for checking unused dependencies."""

from invoke import task
from invoke.collection import Collection
from invoke.context import Context


@task
def check(context: Context) -> None:
    """Run deptry to check for unused dependencies."""
    context.run("poetry run deptry .", echo=True)


collection = Collection("deptry")
collection.add_task(check, "check")
