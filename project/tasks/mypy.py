"""MyPy tasks for type checking."""

from invoke import task
from invoke.collection import Collection
from invoke.context import Context


@task
def check(context: Context) -> None:
    """Run mypy to check for type errors."""
    context.run("poetry run mypy .", echo=True)


collection = Collection("mypy")
collection.add_task(check, "check")
