"""Invoke task collections for project development tasks."""

from invoke import task
from invoke.collection import Collection
from invoke.context import Context

ns = Collection()


@task
def run_actionlint(context: Context) -> None:
    """Run actionlint to check GitHub Actions workflows."""
    context.run("poetry run actionlint")


actionlint = Collection("actionlint")
actionlint.add_task(run_actionlint, "check")
ns.add_collection(actionlint)


@task
def run_deptry(context: Context) -> None:
    """Run deptry to check for unused dependencies."""
    context.run("poetry run deptry .")


deptry = Collection("deptry")
deptry.add_task(run_deptry, "check")
ns.add_collection(deptry)


@task
def run_mypy(context: Context) -> None:
    """Run mypy to check for type errors."""
    context.run("poetry run mypy .")


mypy = Collection("mypy")
mypy.add_task(run_mypy, "check")
ns.add_collection(mypy)


@task
def run_precommit(context: Context) -> None:
    """Run pre-commit checks."""
    context.run("poetry run pre-commit run --all-files")


precommit = Collection("precommit")
precommit.add_task(run_precommit, "check")
ns.add_collection(precommit)


@task
def run_ruff_lint(context: Context, *, apply_safe_fixes: bool = False, apply_unsafe_fixes: bool = False) -> None:
    """Run ruff to check for code style issues."""
    if apply_safe_fixes:
        context.run("poetry run ruff check . --fix ")
    elif apply_unsafe_fixes:
        context.run("poetry run ruff check . --unsafe-fixes")
    else:
        context.run("poetry run ruff check . --no-fix")


@task
def run_ruff_format(context: Context, *, apply_safe_fixes: bool = False) -> None:
    """Run ruff to format code."""
    if apply_safe_fixes:
        context.run("poetry run ruff format . --no-preview")
    else:
        context.run("poetry run ruff format . --check")


ruff = Collection("ruff")
ruff.add_task(run_ruff_lint, "lint")
ruff.add_task(run_ruff_format, "format")
ns.add_collection(ruff)


@task
def run_pipaudit(context: Context) -> None:
    """Run pip-audit to check for vulnerable dependencies."""
    context.run("mkdir -p .penguin/pipaudit")
    context.run(
        "poetry export --format=requirements.txt --without-hashes --only main "
        "-o .penguin/pipaudit/requirements-main.txt"
    )
    context.run(
        "poetry export --format=requirements.txt --without-hashes --without main "
        "-o .penguin/pipaudit/requirements-dev.txt"
    )
    context.run("poetry run pip-audit -r .penguin/pipaudit/requirements-main.txt")
    context.run("poetry run pip-audit -r .penguin/pipaudit/requirements-dev.txt")


pipaudit = Collection("pipaudit")
pipaudit.add_task(run_pipaudit, "check")
ns.add_collection(pipaudit)


@task
def run_unit_tests(context: Context) -> None:
    """Run unit tests using pytest."""
    context.run(
        "poetry run pytest tests/unit/ --disable-socket --cov=src "
        "--cov-config=.unit-test-coveragerc --cov-report term-missing --cov-report term:skip-covered"
    )


@task
def run_integration_tests(context: Context) -> None:
    """Run integration tests using pytest."""
    context.run(
        "poetry run pytest tests/integration/ --disable-socket --cov=src "
        "--cov-config=.integration-test-coveragerc --cov-report term-missing --cov-report term:skip-covered"
    )


@task
def run_tox(context: Context) -> None:
    """Run multi-version testing using tox."""
    context.run("poetry run tox")


tests = Collection("tests")
tests.add_task(run_unit_tests, "unit")
tests.add_task(run_integration_tests, "integration")
tests.add_task(run_tox, "tox")
ns.add_collection(tests)


@task
def run_vulture(context: Context) -> None:
    """Run vulture to check for unused code."""
    context.run("poetry run vulture . vulture_whitelist")


vulture = Collection("vulture")
vulture.add_task(run_vulture, "check")
ns.add_collection(vulture)


@task
def run_xenon(context: Context) -> None:
    """Run xenon to check for code complexity."""
    context.run("poetry run xenon --max-absolute B --max-modules A --max-average A .")


xenon = Collection("xenon")
xenon.add_task(run_xenon, "check")
ns.add_collection(xenon)


@task
def update(context: Context) -> None:
    """Update all dependencies and pre-commit hooks."""
    context.run("poetry update")
    context.run("poetry run pre-commit autoupdate")
    context.run("claude -p /init --permission-mode acceptEdits")


@task
def project_check(context: Context, *, apply_safe_fixes: bool = False, apply_unsafe_fixes: bool = False) -> None:
    """Run all project checks."""
    # run_actionlint(context) # noqa: ERA001 Needs actionlint adding to github
    run_deptry(context)
    run_mypy(context)
    run_precommit(context)
    run_ruff_format(context, apply_safe_fixes=apply_safe_fixes)
    run_ruff_lint(context, apply_safe_fixes=apply_safe_fixes, apply_unsafe_fixes=apply_unsafe_fixes)
    run_pipaudit(context)
    run_vulture(context)
    run_xenon(context)
    run_unit_tests(context)
    run_integration_tests(context)


project = Collection("project")
project.add_task(update)
project.add_task(project_check, "check")
ns.add_collection(project)
