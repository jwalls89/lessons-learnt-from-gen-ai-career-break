"""Task runner for orchestrating multiple project tasks with banners and skip functionality."""

from dataclasses import dataclass
from typing import Any

from invoke.context import Context
from invoke.tasks import Task


@dataclass
class ProjectTask:
    """Represents a project task to be executed.

    Attributes:
        name: The display name of the task.
        func: The invoke task to execute.
        kwargs: Keyword arguments to pass to the task function.

    """

    name: str
    func: Task
    kwargs: dict[str, Any]


class ProjectTaskRunner:
    """Orchestrates execution of multiple tasks with banner output and skip functionality.

    Attributes:
        context: The invoke context for running tasks.
        tasks: List of ProjectTask instances to execute.
        skip_list: List of task names to skip.
        executed: List of task names that were executed.
        skipped: List of task names that were skipped.

    """

    def __init__(
        self,
        context: Context,
        tasks: list[ProjectTask],
        skip: list[str] | None = None,
    ) -> None:
        """Initialize the task runner.

        Args:
            context: The invoke context for running tasks.
            tasks: List of ProjectTask instances to execute.
            skip: Optional list of task names to skip.

        """
        self.context = context
        self.tasks = tasks
        self.skip_list = skip or []
        self.executed: list[str] = []
        self.skipped: list[str] = []

    def run(self) -> None:
        """Execute all configured tasks and print summary."""
        for task in self.tasks:
            if task.name in self.skip_list:
                self._skip_task(task.name)
            else:
                self._execute_task(task)

        self._print_summary()

    def _execute_task(self, task: ProjectTask) -> None:
        """Execute a single task with banner.

        Args:
            task: The ProjectTask to execute.

        """
        self._print_banner(task.name)
        task.func(self.context, **task.kwargs)
        self.executed.append(task.name)

    def _skip_task(self, task_name: str) -> None:
        """Skip a task and track it.

        Args:
            task_name: The name of the task to skip.

        """
        print(f"\n⊘ Skipping: {task_name}")
        self.skipped.append(task_name)

    def _print_banner(self, task_name: str) -> None:
        """Print a banner for the task being executed.

        Args:
            task_name: The name of the task being run.

        """
        print(f"\n{'=' * 60}")
        print(f"Running: {task_name}")
        print("=" * 60)

    def _print_summary(self) -> None:
        """Print a summary of executed and skipped tasks."""
        print(f"\n{'=' * 60}")
        print("SUMMARY")
        print("=" * 60)
        print(f"✓ Completed: {len(self.executed)} task(s)")
        if self.executed:
            for task_name in self.executed:
                print(f"  - {task_name}")

        if self.skipped:
            print(f"\n⊘ Skipped: {len(self.skipped)} task(s)")
            for task_name in self.skipped:
                print(f"  - {task_name}")

        print("=" * 60)
