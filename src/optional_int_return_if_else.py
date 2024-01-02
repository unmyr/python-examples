"""An example of return if-else."""
import typing


# tag::content[]
def optional_int(num_str: typing.Optional[str]) -> typing.Optional[int]:
    """Optional[str] to Optional[int]."""
    return None if num_str is None else int(num_str)


# end::content[]


def main() -> None:
    """Run main."""
    assert optional_int(None) is None
    assert optional_int("123") == 123


if __name__ == "__main__":
    main()
