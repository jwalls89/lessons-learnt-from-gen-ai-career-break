"""Vulture tasks for checking unused code."""

from invoke import task
from invoke.collection import Collection
from invoke.context import Context


@task
def check(context: Context) -> None:
    """Run vulture to check for unused code."""
    context.run("poetry run vulture . vulture_whitelist", echo=True)


@task
def regenerate(context: Context) -> None:
    """Regenerate the vulture whitelist file."""
    context.run("poetry run vulture . --make-whitelist > vulture_whitelist", echo=True)


whitelist_collection = Collection("whitelist")
whitelist_collection.add_task(regenerate, "regenerate")

collection = Collection("vulture")
collection.add_task(check, "check")
collection.add_collection(whitelist_collection)
