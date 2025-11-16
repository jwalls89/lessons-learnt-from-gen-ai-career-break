"""Unit tests for the project module."""

from unittest.mock import ANY

import pytest
from invoke.context import Context
from pytest_mock import MockerFixture

from project.project import check, update
from project.project_task_runner import ProjectTask, ProjectTaskRunner
from project.tasks import deptry, mypy, pipaudit, poetry, precommit, ruff, testing, trivy, vulture, xenon


class TestUpdate:
    """Test suite for the update task."""

    @pytest.fixture(autouse=True)
    def _setup(self, mocker: MockerFixture) -> None:
        """Set up common mocks for all update tests."""
        self.mock_context = mocker.Mock(spec_set=Context)
        self.mock_runner = mocker.Mock(spec_set=ProjectTaskRunner)
        self.mock_runner_class = mocker.patch("project.project.ProjectTaskRunner", return_value=self.mock_runner)

    def test_update_creates_runner_with_correct_tasks(self) -> None:
        """Test that update creates a ProjectTaskRunner with poetry and precommit tasks."""
        update(self.mock_context)

        self.mock_runner_class.assert_called_once_with(
            self.mock_context,
            [
                ProjectTask(name="poetry.update", func=poetry.update, kwargs={}),
                ProjectTask(name="precommit.update", func=precommit.update, kwargs={}),
            ],
            None,
        )
        self.mock_runner.run.assert_called_once()

    def test_update_passes_skip_list_to_runner(self) -> None:
        """Test that update passes skip list to the runner."""
        skip_list = ["poetry.update"]
        update(self.mock_context, skip=skip_list)

        self.mock_runner_class.assert_called_once_with(
            self.mock_context,
            [
                ProjectTask(name="poetry.update", func=poetry.update, kwargs={}),
                ProjectTask(name="precommit.update", func=precommit.update, kwargs={}),
            ],
            skip_list,
        )


class TestCheck:
    """Test suite for the check task."""

    @pytest.fixture(autouse=True)
    def _setup(self, mocker: MockerFixture) -> None:
        """Set up common mocks for all check tests."""
        self.mock_context = mocker.Mock(spec_set=Context)
        self.mock_runner = mocker.Mock(spec_set=ProjectTaskRunner)
        self.mock_runner_class = mocker.patch("project.project.ProjectTaskRunner", return_value=self.mock_runner)

    def test_check_creates_runner_with_all_check_tasks(self) -> None:
        """Test that check creates a ProjectTaskRunner with all check tasks."""
        check(self.mock_context)

        self.mock_runner_class.assert_called_once_with(
            self.mock_context,
            [
                ProjectTask(name="precommit.check", func=precommit.check, kwargs={"apply_safe_fixes": False}),
                ProjectTask(name="ruff.format", func=ruff.format, kwargs={"apply_safe_fixes": False}),
                ProjectTask(
                    name="ruff.lint",
                    func=ruff.lint,
                    kwargs={"apply_safe_fixes": False, "apply_unsafe_fixes": False},
                ),
                ProjectTask(name="mypy.check", func=mypy.check, kwargs={}),
                ProjectTask(name="vulture.check", func=vulture.check, kwargs={}),
                ProjectTask(name="xenon.check", func=xenon.check, kwargs={}),
                ProjectTask(name="tests.unit", func=testing.unit, kwargs={}),
                ProjectTask(name="tests.integration", func=testing.integration, kwargs={}),
                ProjectTask(name="pipaudit.check", func=pipaudit.check, kwargs={}),
                ProjectTask(name="deptry.check", func=deptry.check, kwargs={}),
                ProjectTask(name="trivy.check", func=trivy.check, kwargs={}),
            ],
            None,
        )
        self.mock_runner.run.assert_called_once()

    def test_check_passes_apply_safe_fixes_to_precommit_and_ruff_tasks(self) -> None:
        """Test that check passes apply_safe_fixes parameter to precommit and ruff tasks."""
        check(self.mock_context, apply_safe_fixes=True)

        tasks_list = self.mock_runner_class.call_args[0][1]
        precommit_check_task = next(task for task in tasks_list if task.name == "precommit.check")
        ruff_format_task = next(task for task in tasks_list if task.name == "ruff.format")
        ruff_lint_task = next(task for task in tasks_list if task.name == "ruff.lint")

        assert precommit_check_task.kwargs == {"apply_safe_fixes": True}
        assert ruff_format_task.kwargs == {"apply_safe_fixes": True}
        assert ruff_lint_task.kwargs == {"apply_safe_fixes": True, "apply_unsafe_fixes": False}

    def test_check_passes_apply_unsafe_fixes_to_ruff_lint(self) -> None:
        """Test that check passes apply_unsafe_fixes parameter to ruff.lint."""
        check(self.mock_context, apply_unsafe_fixes=True)

        tasks_list = self.mock_runner_class.call_args[0][1]
        ruff_lint_task = next(task for task in tasks_list if task.name == "ruff.lint")

        assert ruff_lint_task.kwargs == {"apply_safe_fixes": False, "apply_unsafe_fixes": True}

    def test_check_passes_skip_list_to_runner(self) -> None:
        """Test that check passes skip list to the runner."""
        skip_list = ["mypy.check", "testing.unit"]
        check(self.mock_context, skip=skip_list)

        self.mock_runner_class.assert_called_once_with(ANY, ANY, skip_list)
