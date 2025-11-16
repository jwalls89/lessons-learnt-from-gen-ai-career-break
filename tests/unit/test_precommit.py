"""Unit tests for the precommit module."""

from unittest.mock import Mock

from invoke.context import Context

from project.precommit import check


class TestPrecommit:
    """Test suite for the check function."""

    def test_check_runs_precommit_with_echo_when_invoked(self) -> None:
        """Test that check runs pre-commit command with echo enabled."""
        mock_context = Mock(spec_set=Context)

        check(mock_context)

        mock_context.run.assert_called_once_with("poetry run pre-commit run --all-files", echo=True)
