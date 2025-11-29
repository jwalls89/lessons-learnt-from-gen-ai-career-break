"""Unit tests for the devcontainer module."""

from pathlib import Path
from unittest.mock import Mock, call

import pytest
from invoke.context import Context
from pytest_mock import MockerFixture

from project.tasks.devcontainer import check


class TestDevcontainer:
    """Test suite for the devcontainer check function."""

    @pytest.fixture(autouse=True)
    def setup_fixture(self, mocker: MockerFixture) -> None:
        """Set up common mocks for devcontainer tests."""
        self.mock_workspace_path = Path("/mock/workspace")
        mocker.patch("project.tasks.devcontainer.get_current_working_directory", return_value=self.mock_workspace_path)
        self.mock_context = Mock(spec_set=Context)

    def test_check_runs_build_up_and_exec_with_invoke_list_by_default(self) -> None:
        """Test that check runs build, up, and exec with invoke --list when no flags provided."""
        check(self.mock_context)

        assert self.mock_context.run.call_count == 4
        self.mock_context.run.assert_has_calls(
            [
                call("docker info", hide=True),
                call(f"npx @devcontainers/cli build --workspace-folder {self.mock_workspace_path}", echo=True),
                call(f"npx @devcontainers/cli up --workspace-folder {self.mock_workspace_path}", echo=True),
                call(
                    f"npx @devcontainers/cli exec --workspace-folder {self.mock_workspace_path} "
                    f"poetry run invoke --list",
                    echo=True,
                ),
            ]
        )

    def test_check_only_runs_build_when_build_only_flag_is_true(self) -> None:
        """Test that check only runs docker info and build when build_only is True."""
        check(self.mock_context, build_only=True)

        assert self.mock_context.run.call_count == 2
        self.mock_context.run.assert_has_calls(
            [
                call("docker info", hide=True),
                call(f"npx @devcontainers/cli build --workspace-folder {self.mock_workspace_path}", echo=True),
            ]
        )

    def test_check_runs_project_check_when_run_project_check_flag_is_true(self) -> None:
        """Test that check runs invoke project.check instead of invoke --list when run_project_check is True."""
        check(self.mock_context, run_project_check=True)

        assert self.mock_context.run.call_count == 4
        self.mock_context.run.assert_has_calls(
            [
                call("docker info", hide=True),
                call(f"npx @devcontainers/cli build --workspace-folder {self.mock_workspace_path}", echo=True),
                call(f"npx @devcontainers/cli up --workspace-folder {self.mock_workspace_path}", echo=True),
                call(
                    f"npx @devcontainers/cli exec --workspace-folder {self.mock_workspace_path} "
                    f"poetry run invoke project.check",
                    echo=True,
                ),
            ]
        )

    def test_check_only_builds_when_both_build_only_and_run_project_check_are_true(self) -> None:
        """Test that build_only takes precedence when both flags are True."""
        check(self.mock_context, build_only=True, run_project_check=True)

        assert self.mock_context.run.call_count == 2
        self.mock_context.run.assert_has_calls(
            [
                call("docker info", hide=True),
                call(f"npx @devcontainers/cli build --workspace-folder {self.mock_workspace_path}", echo=True),
            ]
        )
