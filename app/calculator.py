"""Calculator business logic module."""


class DivisionByZeroError(Exception):
    """Raised when attempting to divide by zero."""

    def __init__(self, message: str = "Division by zero is not allowed") -> None:
        self.message = message
        super().__init__(self.message)


def add(a: float, b: float) -> float:
    """Add two numbers.

    Args:
        a: First number.
        b: Second number.

    Returns:
        Sum of a and b.
    """
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtract two numbers.

    Args:
        a: First number.
        b: Second number.

    Returns:
        Difference of a and b.
    """
    return a - b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers.

    Args:
        a: First number.
        b: Second number.

    Returns:
        Product of a and b.
    """
    return a * b


def divide(a: float, b: float) -> float:
    """Divide two numbers.

    Args:
        a: Dividend.
        b: Divisor.

    Returns:
        Quotient of a and b.

    Raises:
        DivisionByZeroError: If b is zero.
    """
    if b == 0:
        raise DivisionByZeroError()
    return a / b
