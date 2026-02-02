"""Unit tests for calculator business logic."""

import pytest

from app.calculator import DivisionByZeroError, add, divide, multiply, subtract


class TestAdd:
    """Test cases for add function."""

    def test_add_positive_numbers(self) -> None:
        """Test addition of two positive numbers."""
        assert add(2, 3) == 5

    def test_add_negative_numbers(self) -> None:
        """Test addition of two negative numbers."""
        assert add(-2, -3) == -5

    def test_add_mixed_numbers(self) -> None:
        """Test addition of positive and negative numbers."""
        assert add(-2, 3) == 1

    def test_add_floats(self) -> None:
        """Test addition of floating point numbers."""
        assert add(2.5, 3.5) == 6.0

    def test_add_zero(self) -> None:
        """Test addition with zero."""
        assert add(5, 0) == 5


class TestSubtract:
    """Test cases for subtract function."""

    def test_subtract_positive_numbers(self) -> None:
        """Test subtraction of two positive numbers."""
        assert subtract(5, 3) == 2

    def test_subtract_negative_numbers(self) -> None:
        """Test subtraction of two negative numbers."""
        assert subtract(-5, -3) == -2

    def test_subtract_mixed_numbers(self) -> None:
        """Test subtraction of positive and negative numbers."""
        assert subtract(5, -3) == 8

    def test_subtract_floats(self) -> None:
        """Test subtraction of floating point numbers."""
        assert subtract(5.5, 2.5) == 3.0

    def test_subtract_zero(self) -> None:
        """Test subtraction with zero."""
        assert subtract(5, 0) == 5


class TestMultiply:
    """Test cases for multiply function."""

    def test_multiply_positive_numbers(self) -> None:
        """Test multiplication of two positive numbers."""
        assert multiply(4, 3) == 12

    def test_multiply_negative_numbers(self) -> None:
        """Test multiplication of two negative numbers."""
        assert multiply(-4, -3) == 12

    def test_multiply_mixed_numbers(self) -> None:
        """Test multiplication of positive and negative numbers."""
        assert multiply(-4, 3) == -12

    def test_multiply_floats(self) -> None:
        """Test multiplication of floating point numbers."""
        assert multiply(2.5, 4) == 10.0

    def test_multiply_zero(self) -> None:
        """Test multiplication with zero."""
        assert multiply(5, 0) == 0


class TestDivide:
    """Test cases for divide function."""

    def test_divide_positive_numbers(self) -> None:
        """Test division of two positive numbers."""
        assert divide(10, 2) == 5

    def test_divide_negative_numbers(self) -> None:
        """Test division of two negative numbers."""
        assert divide(-10, -2) == 5

    def test_divide_mixed_numbers(self) -> None:
        """Test division of positive and negative numbers."""
        assert divide(-10, 2) == -5

    def test_divide_floats(self) -> None:
        """Test division of floating point numbers."""
        assert divide(7.5, 2.5) == 3.0

    def test_divide_by_zero_raises_error(self) -> None:
        """Test that division by zero raises DivisionByZeroError."""
        with pytest.raises(DivisionByZeroError) as exc_info:
            divide(10, 0)
        assert exc_info.value.message == "Division by zero is not allowed"

    def test_divide_zero_by_number(self) -> None:
        """Test division of zero by a number."""
        assert divide(0, 5) == 0
