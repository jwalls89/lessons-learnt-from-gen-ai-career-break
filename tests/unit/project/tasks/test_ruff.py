"""Unit tests for the ruff module."""

from unittest.mock import Mock

from invoke.context import Context

from project.tasks.ruff import format as ruff_format
from project.tasks.ruff import lint


class TestRuff:
    """Test suite for the ruff module functions."""

    def test_lint_runs_check_with_no_fix_when_no_parameters_provided(self) -> None:
        """Test that lint runs ruff check with --no-fix when called without parameters."""
        mock_context = Mock(spec_set=Context)

        lint(mock_context)

        mock_context.run.assert_called_once_with("poetry run ruff check . --no-fix", echo=True)

    def test_lint_runs_check_with_fix_when_apply_safe_fixes_is_true(self) -> None:
        """Test that lint runs ruff check with --fix when apply_safe_fixes is True."""
        mock_context = Mock(spec_set=Context)

        lint(mock_context, apply_safe_fixes=True)

        mock_context.run.assert_called_once_with("poetry run ruff check . --fix ", echo=True)

    def test_lint_runs_check_with_unsafe_fixes_when_apply_unsafe_fixes_is_true(self) -> None:
        """Test that lint runs ruff check with --unsafe-fixes when apply_unsafe_fixes is True."""
        mock_context = Mock(spec_set=Context)

        lint(mock_context, apply_unsafe_fixes=True)

        mock_context.run.assert_called_once_with("poetry run ruff check . --unsafe-fixes", echo=True)

    def test_format_runs_check_when_no_parameters_provided(self) -> None:
        """Test that format runs ruff format with --check when called without parameters."""
        mock_context = Mock(spec_set=Context)

        ruff_format(mock_context)

        mock_context.run.assert_called_once_with("poetry run ruff format . --check", echo=True)

    def test_format_runs_with_no_preview_when_apply_safe_fixes_is_true(self) -> None:
        """Test that format runs ruff format with --no-preview when apply_safe_fixes is True."""
        mock_context = Mock(spec_set=Context)

        ruff_format(mock_context, apply_safe_fixes=True)

        mock_context.run.assert_called_once_with("poetry run ruff format . --no-preview", echo=True)
