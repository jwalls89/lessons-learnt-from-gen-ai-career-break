"""Unit tests for the vulture module."""

from unittest.mock import Mock

from invoke.context import Context

from project.vulture import check


class TestVulture:
    """Test suite for the check function."""

    def test_check_runs_vulture_with_echo_when_invoked(self) -> None:
        """Test that check runs vulture command with echo enabled."""
        mock_context = Mock(spec_set=Context)

        check(mock_context)

        mock_context.run.assert_called_once_with("poetry run vulture . vulture_whitelist", echo=True)
