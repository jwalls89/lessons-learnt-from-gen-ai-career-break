"""Project-level tasks for updating dependencies and running all checks."""

from invoke import task
from invoke.collection import Collection
from invoke.context import Context

from project.project_task_runner import ProjectTask, ProjectTaskRunner
from project.tasks import deptry, mypy, pipaudit, poetry, precommit, ruff, testing, vulture, xenon


@task(iterable=["skip"])
def update(context: Context, skip: list[str] | None = None) -> None:
    """Update all dependencies and pre-commit hooks.

    Args:
        context: The invoke context.
        skip: Optional list of task names to skip (use --skip taskname multiple times).

    """
    tasks = [
        ProjectTask(name="poetry.update", func=poetry.update, kwargs={}),
        ProjectTask(name="precommit.update", func=precommit.update, kwargs={}),
    ]

    runner = ProjectTaskRunner(context, tasks, skip)
    runner.run()


@task(iterable=["skip"])
def check(
    context: Context,
    skip: list[str] | None = None,
    *,
    apply_safe_fixes: bool = False,
    apply_unsafe_fixes: bool = False,
) -> None:
    """Run all project checks.

    Args:
        context: The invoke context.
        skip: Optional list of task names to skip (use --skip taskname multiple times).
        apply_safe_fixes: Whether to apply safe fixes for ruff.
        apply_unsafe_fixes: Whether to apply unsafe fixes for ruff.

    """
    tasks = [
        # ProjectTask(name="actionlint.check", func=actionlint.check, kwargs={}),  # noqa: ERA001
        ProjectTask(name="precommit.check", func=precommit.check, kwargs={}),
        ProjectTask(name="ruff.format", func=ruff.format, kwargs={"apply_safe_fixes": apply_safe_fixes}),
        ProjectTask(
            name="ruff.lint",
            func=ruff.lint,
            kwargs={"apply_safe_fixes": apply_safe_fixes, "apply_unsafe_fixes": apply_unsafe_fixes},
        ),
        ProjectTask(name="mypy.check", func=mypy.check, kwargs={}),
        ProjectTask(name="vulture.check", func=vulture.check, kwargs={}),
        ProjectTask(name="xenon.check", func=xenon.check, kwargs={}),
        ProjectTask(name="testing.unit", func=testing.unit, kwargs={}),
        ProjectTask(name="testing.integration", func=testing.integration, kwargs={}),
        ProjectTask(name="pipaudit.check", func=pipaudit.check, kwargs={}),
        ProjectTask(name="deptry.check", func=deptry.check, kwargs={}),
    ]

    runner = ProjectTaskRunner(context, tasks, skip)
    runner.run()


collection = Collection("project")
collection.add_task(update)
collection.add_task(check)
