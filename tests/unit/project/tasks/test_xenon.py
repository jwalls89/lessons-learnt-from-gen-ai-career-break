"""Unit tests for the xenon module."""

from unittest.mock import Mock

from invoke.context import Context

from project.tasks.xenon import check


class TestXenon:
    """Test suite for the check function."""

    def test_check_runs_xenon_with_echo_when_invoked(self) -> None:
        """Test that check runs xenon command with echo enabled."""
        mock_context = Mock(spec_set=Context)

        check(mock_context)

        mock_context.run.assert_called_once_with(
            "poetry run xenon --max-absolute B --max-modules A --max-average A .", echo=True
        )
