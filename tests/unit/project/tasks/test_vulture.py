"""Unit tests for the vulture module."""

from unittest.mock import Mock

from invoke.context import Context

from project.tasks.vulture import check, regenerate


class TestVulture:
    """Test suite for the vulture module functions."""

    def test_check_runs_vulture_with_echo_when_invoked(self) -> None:
        """Test that check runs vulture command with echo enabled."""
        mock_context = Mock(spec_set=Context)

        check(mock_context)

        mock_context.run.assert_called_once_with("poetry run vulture . vulture_whitelist", echo=True)

    def test_regenerate_runs_vulture_make_whitelist_with_echo_when_invoked(self) -> None:
        """Test that regenerate runs vulture command with --make-whitelist and echo enabled."""
        mock_context = Mock(spec_set=Context)

        regenerate(mock_context)

        mock_context.run.assert_called_once_with("poetry run vulture . --make-whitelist > vulture_whitelist", echo=True)
