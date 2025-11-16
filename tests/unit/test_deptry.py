"""Unit tests for the deptry module."""

from unittest.mock import Mock

from invoke.context import Context

from project.deptry import check


class TestDeptry:
    """Test suite for the check function."""

    def test_check_runs_deptry_with_echo_when_invoked(self) -> None:
        """Test that check runs deptry command with echo enabled."""
        mock_context = Mock(spec_set=Context)

        check(mock_context)

        mock_context.run.assert_called_once_with("poetry run deptry .", echo=True)
