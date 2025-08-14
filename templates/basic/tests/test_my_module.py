from my_package.my_module import add, main


def test_main() -> None:
    """Test the main method runs through without exception."""
    # when
    main()

    # then
    # no exception -> pass


def test_add() -> None:
    """Test addition of two numbers."""
    # when
    assert add(1.2, 2.3) == 3.5  # noqa: PLR2004
