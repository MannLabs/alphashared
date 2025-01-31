from src.hello_world import main


def test_main() -> None:
    """Test the main method runs through without exception."""
    # when
    main()

    # then
    # no exception -> pass
