"""Testing tasks for unit, integration, and multi-version testing."""

from invoke import task
from invoke.collection import Collection
from invoke.context import Context


@task
def unit(context: Context) -> None:
    """Run unit tests using pytest."""
    context.run(
        "poetry run pytest tests/unit/ --disable-socket --cov=src --cov=project "
        "--cov-config=.unit-test-coveragerc --cov-report term-missing --cov-report term:skip-covered",
        echo=True,
    )


@task
def integration(context: Context) -> None:
    """Run integration tests using pytest."""
    context.run(
        "poetry run pytest tests/integration/ --disable-socket --cov=src "
        "--cov-config=.integration-test-coveragerc --cov-report term-missing --cov-report term:skip-covered",
        echo=True,
    )


@task
def tox(context: Context) -> None:
    """Run multi-version testing using tox."""
    context.run("poetry run tox", echo=True)


collection = Collection("tests")
collection.add_task(unit)
collection.add_task(integration)
collection.add_task(tox)
