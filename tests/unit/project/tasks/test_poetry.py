"""Unit tests for the poetry module."""

from unittest.mock import Mock

from invoke.context import Context

from project.tasks.poetry import update


class TestPoetry:
    """Test suite for the poetry module functions."""

    def test_update_runs_poetry_update_with_echo_when_invoked(self) -> None:
        """Test that update runs poetry update command with echo enabled."""
        mock_context = Mock(spec_set=Context)

        update(mock_context)

        mock_context.run.assert_called_once_with("poetry update", echo=True)
