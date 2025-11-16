"""Unit tests for the precommit module."""

from unittest.mock import Mock

from invoke.context import Context

from project.tasks.precommit import check, update


class TestPrecommit:
    """Test suite for the check function."""

    def test_check_runs_precommit_with_echo_when_invoked(self) -> None:
        """Test that check runs pre-commit command with echo enabled."""
        mock_context = Mock(spec_set=Context)

        check(mock_context)

        mock_context.run.assert_called_once_with("poetry run pre-commit run --all-files", echo=True)

    def test_check_runs_precommit_with_apply_safe_fixes_false(self) -> None:
        """Test that check runs only standard pre-commit when apply_safe_fixes is False."""
        mock_context = Mock(spec_set=Context)

        check(mock_context, apply_safe_fixes=False)

        mock_context.run.assert_called_once_with("poetry run pre-commit run --all-files", echo=True)

    def test_check_runs_safe_fixers_and_precommit_with_apply_safe_fixes_true(self) -> None:
        """Test that check runs safe fixers and pre-commit when apply_safe_fixes is True."""
        mock_context = Mock(spec_set=Context)

        check(mock_context, apply_safe_fixes=True)

        assert mock_context.run.call_count == 3
        mock_context.run.assert_any_call(
            "poetry run pre-commit run end-of-file-fixer --all-files", echo=True, warn=True
        )
        mock_context.run.assert_any_call("poetry run pre-commit run md-toc --all-files", echo=True, warn=True)
        mock_context.run.assert_any_call("poetry run pre-commit run --all-files", echo=True)

    def test_update_runs_precommit_autoupdate_with_echo_when_invoked(self) -> None:
        """Test that update runs pre-commit autoupdate command with echo enabled."""
        mock_context = Mock(spec_set=Context)

        update(mock_context)

        mock_context.run.assert_called_once_with("poetry run pre-commit autoupdate", echo=True)
