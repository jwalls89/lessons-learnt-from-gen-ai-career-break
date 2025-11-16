"""Unit tests for the mypy module."""

from unittest.mock import Mock

from invoke.context import Context

from project.mypy import check


class TestMypy:
    """Test suite for the check function."""

    def test_check_runs_mypy_with_echo_when_invoked(self) -> None:
        """Test that check runs mypy command with echo enabled."""
        mock_context = Mock(spec_set=Context)

        check(mock_context)

        mock_context.run.assert_called_once_with("poetry run mypy .", echo=True)
