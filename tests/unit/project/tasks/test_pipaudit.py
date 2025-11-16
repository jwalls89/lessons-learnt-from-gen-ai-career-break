"""Unit tests for the pipaudit module."""

from unittest.mock import Mock, call

from invoke.context import Context
from pytest_mock import MockerFixture

from project.tasks.pipaudit import check


class TestPipaudit:
    """Test suite for the check function."""

    def test_check_runs_all_commands_in_sequence_when_invoked(self, mocker: MockerFixture) -> None:
        """Test that check runs all required commands in correct order with echo enabled."""
        # Mock ensure_directory to prevent filesystem writes during test
        mock_ensure_directory = mocker.patch("project.tasks.pipaudit.ensure_directory")
        mock_context = Mock(spec_set=Context)

        check(mock_context)

        # Verify ensure_directory was called
        mock_ensure_directory.assert_called_once_with(".quality/pipaudit")

        # Verify the poetry commands were called
        expected_calls = [
            call(
                "poetry export --format=requirements.txt --without-hashes -o .quality/pipaudit/requirements.txt",
                echo=True,
            ),
            call("poetry run pip-audit -r .quality/pipaudit/requirements.txt", echo=True),
        ]
        mock_context.run.assert_has_calls(expected_calls, any_order=False)
        assert mock_context.run.call_count == 2
