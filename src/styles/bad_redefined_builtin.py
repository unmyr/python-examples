# -*- coding: utf-8 -*-
"""Bad style example."""


def main():
    """main."""
    # pylint: disable=redefined-builtin
    str: int = 5 * 4
    print(str)


if __name__ == "__main__":
    main()

# EOF
