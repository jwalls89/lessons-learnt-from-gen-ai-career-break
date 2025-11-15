"""Integration tests for the example module."""

from lessons_learnt import greet
from lessons_learnt.example import calculate_sum


class TestExampleIntegration:
    """Integration tests for example functionality."""

    def test_greet_and_calculate_workflow(self) -> None:
        """Test a workflow combining greet and calculate functions."""
        # This is a simple example of an integration test
        # In a real project, this would test interactions between multiple components
        name = "World"
        greeting = greet(name)
        assert greeting == "Hello, World!"

        # Calculate something based on the greeting length
        greeting_length = len(greeting)
        result = calculate_sum(greeting_length, 10)
        assert result == 23  # len("Hello, World!") + 10 = 13 + 10 = 23
