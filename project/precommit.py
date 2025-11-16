"""Pre-commit tasks for running hooks."""

from invoke import task
from invoke.collection import Collection
from invoke.context import Context


@task
def check(context: Context) -> None:
    """Run pre-commit checks."""
    context.run("poetry run pre-commit run --all-files", echo=True)


collection = Collection("precommit")
collection.add_task(check, "check")
