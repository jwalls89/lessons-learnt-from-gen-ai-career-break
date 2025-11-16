"""Unit tests for the testing module."""

from unittest.mock import Mock

from invoke.context import Context

from project.tasks.testing import integration, tox, unit


class TestTesting:
    """Test suite for the testing module functions."""

    def test_unit_runs_pytest_with_coverage_when_invoked(self) -> None:
        """Test that unit runs pytest with unit test configuration and echo enabled."""
        mock_context = Mock(spec_set=Context)

        unit(mock_context)

        expected_command = (
            "poetry run pytest tests/unit/ --disable-socket --cov=src --cov=project "
            "--cov-config=.unit-test-coveragerc --cov-report term-missing --cov-report term:skip-covered"
        )
        mock_context.run.assert_called_once_with(expected_command, echo=True)

    def test_integration_runs_pytest_with_coverage_when_invoked(self) -> None:
        """Test that integration runs pytest with integration test configuration and echo enabled."""
        mock_context = Mock(spec_set=Context)

        integration(mock_context)

        expected_command = (
            "poetry run pytest tests/integration/ --disable-socket --cov=src "
            "--cov-config=.integration-test-coveragerc --cov-report term-missing --cov-report term:skip-covered"
        )
        mock_context.run.assert_called_once_with(expected_command, echo=True)

    def test_tox_runs_tox_with_echo_when_invoked(self) -> None:
        """Test that tox runs tox command with echo enabled."""
        mock_context = Mock(spec_set=Context)

        tox(mock_context)

        mock_context.run.assert_called_once_with("poetry run tox", echo=True)
