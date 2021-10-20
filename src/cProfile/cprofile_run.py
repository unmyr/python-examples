"""Example of cProfile."""
import cProfile
import pstats
import time


def my_sleep(sec: float) -> None:
    """Sleep wrapper"""
    time.sleep(sec)


def main() -> None:
    """Run main."""
    pr: cProfile.Profile = cProfile.Profile()
    pr.run('my_sleep(1)')

    stats: pstats.Stats = pstats.Stats(pr)
    stats.print_callers()

    stats.sort_stats('cumulative')
    stats.print_stats(100)

    return None


if __name__ == '__main__':
    main()

# EOF
