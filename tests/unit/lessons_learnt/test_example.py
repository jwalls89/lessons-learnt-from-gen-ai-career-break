"""Unit tests for the example module."""

import pytest

from lessons_learnt.example import calculate_sum, greet


class TestGreet:
    """Test suite for the greet function."""

    def test_greet_with_valid_name(self) -> None:
        """Test greeting with a valid name."""
        result = greet("World")
        assert result == "Hello, World!"

    def test_greet_with_different_name(self) -> None:
        """Test greeting with a different name."""
        result = greet("Alice")
        assert result == "Hello, Alice!"

    def test_greet_with_empty_string_raises_error(self) -> None:
        """Test that greeting with an empty string raises ValueError."""
        with pytest.raises(ValueError, match="Name cannot be empty"):
            greet("")


class TestCalculateSum:
    """Test suite for the calculate_sum function."""

    def test_calculate_sum_positive_numbers(self) -> None:
        """Test sum of two positive numbers."""
        result = calculate_sum(2, 3)
        assert result == 5

    def test_calculate_sum_negative_numbers(self) -> None:
        """Test sum of two negative numbers."""
        result = calculate_sum(-2, -3)
        assert result == -5

    def test_calculate_sum_mixed_numbers(self) -> None:
        """Test sum of positive and negative numbers."""
        result = calculate_sum(5, -3)
        assert result == 2

    def test_calculate_sum_with_zero(self) -> None:
        """Test sum with zero."""
        result = calculate_sum(0, 5)
        assert result == 5
