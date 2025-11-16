"""Invoke task collections for project development tasks."""

from invoke import task
from invoke.collection import Collection
from invoke.context import Context

# Import Phase 2 modules
from project import actionlint, deptry, mypy, precommit, vulture, xenon

ns = Collection()

# Add Phase 2 collections
ns.add_collection(actionlint.collection)
ns.add_collection(deptry.collection)
ns.add_collection(mypy.collection)
ns.add_collection(precommit.collection)


@task
def run_ruff_lint(context: Context, *, apply_safe_fixes: bool = False, apply_unsafe_fixes: bool = False) -> None:
    """Run ruff to check for code style issues."""
    if apply_safe_fixes:
        context.run("poetry run ruff check . --fix ", echo=True)
    elif apply_unsafe_fixes:
        context.run("poetry run ruff check . --unsafe-fixes", echo=True)
    else:
        context.run("poetry run ruff check . --no-fix", echo=True)


@task
def run_ruff_format(context: Context, *, apply_safe_fixes: bool = False) -> None:
    """Run ruff to format code."""
    if apply_safe_fixes:
        context.run("poetry run ruff format . --no-preview", echo=True)
    else:
        context.run("poetry run ruff format . --check", echo=True)


ruff = Collection("ruff")
ruff.add_task(run_ruff_lint, "lint")
ruff.add_task(run_ruff_format, "format")
ns.add_collection(ruff)


@task
def run_pipaudit(context: Context) -> None:
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


pipaudit = Collection("pipaudit")
pipaudit.add_task(run_pipaudit, "check")
ns.add_collection(pipaudit)


@task
def run_unit_tests(context: Context) -> None:
    """Run unit tests using pytest."""
    context.run(
        "poetry run pytest tests/unit/ --disable-socket --cov=. "
        "--cov-config=.unit-test-coveragerc --cov-report term-missing --cov-report term:skip-covered",
        echo=True,
    )


@task
def run_integration_tests(context: Context) -> None:
    """Run integration tests using pytest."""
    context.run(
        "poetry run pytest tests/integration/ --disable-socket --cov=src "
        "--cov-config=.integration-test-coveragerc --cov-report term-missing --cov-report term:skip-covered",
        echo=True,
    )


@task
def run_tox(context: Context) -> None:
    """Run multi-version testing using tox."""
    context.run("poetry run tox", echo=True)


tests = Collection("tests")
tests.add_task(run_unit_tests, "unit")
tests.add_task(run_integration_tests, "integration")
tests.add_task(run_tox, "tox")
ns.add_collection(tests)


# Add remaining Phase 2 collections
ns.add_collection(vulture.collection)
ns.add_collection(xenon.collection)


@task
def update(context: Context) -> None:
    """Update all dependencies and pre-commit hooks."""
    context.run("poetry update", echo=True)
    context.run("poetry run pre-commit autoupdate", echo=True)


@task
def project_check(context: Context, *, apply_safe_fixes: bool = False, apply_unsafe_fixes: bool = False) -> None:
    """Run all project checks."""
    # actionlint.check(context) # noqa: ERA001 Needs actionlint adding to github
    deptry.check(context)
    mypy.check(context)
    precommit.check(context)
    run_ruff_format(context, apply_safe_fixes=apply_safe_fixes)
    run_ruff_lint(context, apply_safe_fixes=apply_safe_fixes, apply_unsafe_fixes=apply_unsafe_fixes)
    run_pipaudit(context)
    vulture.check(context)
    xenon.check(context)
    run_unit_tests(context)
    run_integration_tests(context)


project = Collection("project")
project.add_task(update)
project.add_task(project_check, "check")
ns.add_collection(project)
