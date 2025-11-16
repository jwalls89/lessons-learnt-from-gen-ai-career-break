"""Unit tests for the trivy module."""

from unittest.mock import Mock, call

from invoke.context import Context

from project.tasks.trivy import check


class TestTrivy:
    """Test suite for the check function."""

    def test_check_runs_all_commands_in_sequence_when_invoked(self) -> None:
        """Test that check runs all required commands in correct order with echo enabled."""
        mock_context = Mock(spec_set=Context)

        check(mock_context)

        expected_calls = [
            call("mkdir -p .quality/trivy", echo=True),
            call(
                "docker run --rm "
                "-v $(pwd):/workspace "
                "-v $(pwd)/.quality/trivy:/root/.cache/ "
                "aquasec/trivy fs "
                "--scanners vuln,secret,misconfig,license "
                "--exit-code 1 "
                "/workspace",
                echo=True,
            ),
        ]
        mock_context.run.assert_has_calls(expected_calls, any_order=False)
        assert mock_context.run.call_count == 2
