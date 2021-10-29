"""scope example."""
import datetime


def main() -> None:
    """Run main."""
    t_0 = datetime.datetime.now()
    try:
        t_1 = datetime.datetime.now()
    except RuntimeError:
        pass

    print(f"t_0={t_0}, t_1={t_1}")


if __name__ == '__main__':
    main()

# EOF
