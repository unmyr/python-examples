"""Bytes to string."""


def main() -> None:
    """Run main."""
    assert b"Hello world.".decode("utf-8") == "Hello world."


if __name__ == "__main__":
    main()

# EOF
