"""Unit tests for the trivy module."""

from pathlib import Path
from unittest.mock import Mock

from invoke.context import Context
from pytest_mock import MockerFixture

from project.tasks.trivy import check


class TestTrivy:
    """Test suite for the check function."""

    def test_check_runs_all_commands_in_sequence_when_invoked(self, mocker: MockerFixture) -> None:
        """Test that check runs all required commands in correct order with echo enabled."""
        # Mock the utility functions
        mock_workspace_path = Path("/mock/workspace")
        mock_cache_path = mock_workspace_path / ".quality" / "trivy"

        mock_get_cwd = mocker.patch(
            "project.tasks.trivy.get_current_working_directory", return_value=mock_workspace_path
        )
        mock_ensure_directory = mocker.patch("project.tasks.trivy.ensure_directory")

        mock_context = Mock(spec_set=Context)

        check(mock_context)

        # Verify get_current_working_directory was called
        mock_get_cwd.assert_called_once()

        # Verify ensure_directory was called with correct path
        mock_ensure_directory.assert_called_once_with(mock_cache_path)

        # Verify docker command was called with correct paths
        mock_context.run.assert_called_once_with(
            f"docker run --rm "
            f"-v {mock_workspace_path}:/workspace "
            f"-v {mock_cache_path}:/root/.cache/ "
            f"aquasec/trivy fs "
            f"--scanners vuln,secret,misconfig,license "
            f"--exit-code 1 "
            f"/workspace",
            echo=True,
        )
        assert mock_context.run.call_count == 1
