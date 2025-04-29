"""A little test program."""


def main() -> None:
    """The main function."""
    print("Hello world from main!")


def add(a: float, b: float) -> float:
    """Add two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The sum of the two numbers.

    """
    return a + b


if __name__ == "__main__":
    main()
