"""Pip-audit security vulnerability checking tasks."""

from invoke import task
from invoke.collection import Collection
from invoke.context import Context


@task
def check(context: Context) -> None:
    """Run pip-audit to check for vulnerable dependencies."""
    context.run("mkdir -p .quality/pipaudit", echo=True)
    context.run(
        "poetry export --format=requirements.txt --without-hashes --only main "
        "-o .quality/pipaudit/requirements-main.txt",
        echo=True,
    )
    context.run(
        "poetry export --format=requirements.txt --without-hashes --without main "
        "-o .quality/pipaudit/requirements-dev.txt",
        echo=True,
    )
    context.run("poetry run pip-audit -r .quality/pipaudit/requirements-main.txt", echo=True)
    context.run("poetry run pip-audit -r .quality/pipaudit/requirements-dev.txt", echo=True)


collection = Collection("pipaudit")
collection.add_task(check)
