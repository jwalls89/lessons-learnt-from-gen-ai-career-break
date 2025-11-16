"""Unit tests for the actionlint module."""

from unittest.mock import Mock

from invoke.context import Context

from project.tasks.actionlint import check


class TestActionlint:
    """Test suite for the check function."""

    def test_check_runs_actionlint_with_echo_when_invoked(self) -> None:
        """Test that check runs actionlint command with echo enabled."""
        mock_context = Mock(spec_set=Context)

        check(mock_context)

        mock_context.run.assert_called_once_with("poetry run actionlint", echo=True)
