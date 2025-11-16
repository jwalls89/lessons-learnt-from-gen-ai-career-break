"""Unit tests for the pipaudit module."""

from unittest.mock import Mock, call

from invoke.context import Context

from project.tasks.pipaudit import check


class TestPipaudit:
    """Test suite for the check function."""

    def test_check_runs_all_commands_in_sequence_when_invoked(self) -> None:
        """Test that check runs all required commands in correct order with echo enabled."""
        mock_context = Mock(spec_set=Context)

        check(mock_context)

        expected_calls = [
            call("mkdir -p .quality/pipaudit", echo=True),
            call(
                "poetry export --format=requirements.txt --without-hashes --only main "
                "-o .quality/pipaudit/requirements-main.txt",
                echo=True,
            ),
            call(
                "poetry export --format=requirements.txt --without-hashes --without main "
                "-o .quality/pipaudit/requirements-dev.txt",
                echo=True,
            ),
            call("poetry run pip-audit -r .quality/pipaudit/requirements-main.txt", echo=True),
            call("poetry run pip-audit -r .quality/pipaudit/requirements-dev.txt", echo=True),
        ]
        mock_context.run.assert_has_calls(expected_calls, any_order=False)
        assert mock_context.run.call_count == 5
