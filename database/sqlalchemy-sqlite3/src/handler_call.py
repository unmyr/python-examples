"""Example of sqlite3 with SQLAlchemy."""
import handler_serve


def main() -> None:
    """Run main."""
    print(handler_serve.handler())
    print(handler_serve.handler())
    handler_serve.shutdown()


if __name__ == '__main__':
    main()

# EOF
