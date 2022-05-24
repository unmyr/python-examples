"""Uuid example."""
import uuid


def main() -> None:
    """Run main."""
    # make a random UUID
    print(uuid.uuid4())

    # Create UUID with Zeros
    print(uuid.UUID(int=0))


if __name__ == '__main__':
    main()

# EOF
