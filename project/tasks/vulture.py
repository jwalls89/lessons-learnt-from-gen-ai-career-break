"""Vulture tasks for checking unused code."""

from invoke import task
from invoke.collection import Collection
from invoke.context import Context


@task
def check(context: Context) -> None:
    """Run vulture to check for unused code."""
    context.run("poetry run vulture . vulture_whitelist", echo=True)


collection = Collection("vulture")
collection.add_task(check, "check")
