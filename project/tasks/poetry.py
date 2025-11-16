"""Poetry dependency management tasks."""

from invoke import task
from invoke.collection import Collection
from invoke.context import Context


@task
def update(context: Context) -> None:
    """Update all poetry dependencies."""
    context.run("poetry update", echo=True)


collection = Collection("poetry")
collection.add_task(update)
