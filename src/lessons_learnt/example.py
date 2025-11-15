"""Example module to demonstrate project structure."""


def greet(name: str) -> str:
    """Greet a person by name.

    Args:
        name: The name of the person to greet

    Returns:
        A greeting message

    Examples:
        >>> greet("World")
        'Hello, World!'

    """
    if not name:
        msg = "Name cannot be empty"
        raise ValueError(msg)
    return f"Hello, {name}!"


def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        The sum of a and b

    Examples:
        >>> calculate_sum(2, 3)
        5

    """
    return a + b
