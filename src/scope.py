"""scope examples."""


def scope_try_except() -> bool:
    """Exception scope."""
    num1 = 1
    try:
        num2 = 2
    except RuntimeError:
        pass

    return num1 == 1 and num2 == 2


def scope_if_statement(cond: bool) -> bool:
    """if-statement scope."""
    if cond:
        num1 = 0

    return num1 == 0


def main() -> None:
    """Run main."""
    print([
        scope_try_except(),
        scope_if_statement(True)
    ])


if __name__ == '__main__':
    main()

# EOF
