"""Unit tests for the project_task_runner module."""

from invoke import task
from invoke.context import Context
from pytest_mock import MockerFixture

from project.project_task_runner import ProjectTask, ProjectTaskRunner


class TestProjectTask:
    """Test suite for the ProjectTask dataclass."""

    def test_project_task_creation(self, mocker: MockerFixture) -> None:
        """Test that ProjectTask can be created with required attributes."""
        mock_task = mocker.Mock(spec=task)
        kwargs = {"arg1": "value1"}

        project_task = ProjectTask(name="test.task", func=mock_task, kwargs=kwargs)

        assert project_task.name == "test.task"
        assert project_task.func == mock_task
        assert project_task.kwargs == kwargs


class TestProjectTaskRunner:
    """Test suite for the ProjectTaskRunner class."""

    def test_runner_executes_all_tasks_when_no_skip_list(self, mocker: MockerFixture, capsys) -> None:  # noqa: ANN001
        """Test that runner executes all tasks when no skip list is provided."""
        mock_context = mocker.Mock(spec_set=Context)
        mock_task1 = mocker.Mock(spec=task)
        mock_task2 = mocker.Mock(spec=task)

        tasks = [
            ProjectTask(name="task1", func=mock_task1, kwargs={}),
            ProjectTask(name="task2", func=mock_task2, kwargs={"key": "value"}),
        ]

        runner = ProjectTaskRunner(mock_context, tasks)
        runner.run()

        # Verify both tasks were called
        mock_task1.assert_called_once_with(mock_context)
        mock_task2.assert_called_once_with(mock_context, key="value")

        # Verify summary output
        captured = capsys.readouterr()
        assert "✓ Completed: 2 task(s)" in captured.out
        assert "task1" in captured.out
        assert "task2" in captured.out

    def test_runner_skips_tasks_in_skip_list(self, mocker: MockerFixture, capsys) -> None:  # noqa: ANN001
        """Test that runner skips tasks that are in the skip list."""
        mock_context = mocker.Mock(spec_set=Context)
        mock_task1 = mocker.Mock(spec=task)
        mock_task2 = mocker.Mock(spec=task)
        mock_task3 = mocker.Mock(spec=task)

        tasks = [
            ProjectTask(name="task1", func=mock_task1, kwargs={}),
            ProjectTask(name="task2", func=mock_task2, kwargs={}),
            ProjectTask(name="task3", func=mock_task3, kwargs={}),
        ]

        runner = ProjectTaskRunner(mock_context, tasks, skip=["task2"])
        runner.run()

        # Verify task1 and task3 were called, but not task2
        mock_task1.assert_called_once_with(mock_context)
        mock_task2.assert_not_called()
        mock_task3.assert_called_once_with(mock_context)

        # Verify summary output
        captured = capsys.readouterr()
        assert "✓ Completed: 2 task(s)" in captured.out
        assert "⊘ Skipped: 1 task(s)" in captured.out
        assert "task1" in captured.out
        assert "task3" in captured.out

    def test_runner_prints_banner_for_each_task(self, mocker: MockerFixture, capsys) -> None:  # noqa: ANN001
        """Test that runner prints a banner before executing each task."""
        mock_context = mocker.Mock(spec_set=Context)
        mock_task = mocker.Mock(spec=task)

        tasks = [ProjectTask(name="example.task", func=mock_task, kwargs={})]

        runner = ProjectTaskRunner(mock_context, tasks)
        runner.run()

        captured = capsys.readouterr()
        assert "Running: example.task" in captured.out
        assert "=" * 60 in captured.out

    def test_runner_prints_skip_message_for_skipped_tasks(self, mocker: MockerFixture, capsys) -> None:  # noqa: ANN001
        """Test that runner prints a skip message for skipped tasks."""
        mock_context = mocker.Mock(spec_set=Context)
        mock_task = mocker.Mock(spec=task)

        tasks = [ProjectTask(name="skipped.task", func=mock_task, kwargs={})]

        runner = ProjectTaskRunner(mock_context, tasks, skip=["skipped.task"])
        runner.run()

        captured = capsys.readouterr()
        assert "⊘ Skipping: skipped.task" in captured.out
        mock_task.assert_not_called()

    def test_runner_handles_empty_task_list(self, mocker: MockerFixture, capsys) -> None:  # noqa: ANN001
        """Test that runner handles an empty task list gracefully."""
        mock_context = mocker.Mock(spec_set=Context)

        runner = ProjectTaskRunner(mock_context, [])
        runner.run()

        captured = capsys.readouterr()
        assert "✓ Completed: 0 task(s)" in captured.out

    def test_runner_passes_kwargs_to_tasks(self, mocker: MockerFixture) -> None:
        """Test that runner correctly passes kwargs to task functions."""
        mock_context = mocker.Mock(spec_set=Context)
        mock_task = mocker.Mock(spec=task)

        tasks = [
            ProjectTask(
                name="task.with.args",
                func=mock_task,
                kwargs={"arg1": "value1", "arg2": 42, "arg3": True},
            )
        ]

        runner = ProjectTaskRunner(mock_context, tasks)
        runner.run()

        mock_task.assert_called_once_with(mock_context, arg1="value1", arg2=42, arg3=True)
