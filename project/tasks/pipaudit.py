"""Pip-audit security vulnerability checking tasks."""

from invoke import task
from invoke.collection import Collection
from invoke.context import Context

from project.utils import ensure_directory


@task
def check(context: Context) -> None:
    """Run pip-audit to check for vulnerable dependencies."""
    ensure_directory(".quality/pipaudit")
    context.run(
        "poetry export --format=requirements.txt --without-hashes -o .quality/pipaudit/requirements.txt",
        echo=True,
    )
    context.run("poetry run pip-audit -r .quality/pipaudit/requirements.txt", echo=True)


collection = Collection("pipaudit")
collection.add_task(check)
