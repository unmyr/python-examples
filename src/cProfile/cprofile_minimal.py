"""Example of cProfile."""
import cProfile
import pstats


def main() -> None:
    """Run main."""
    pr: cProfile.Profile
    pr = cProfile.Profile()

    pr.enable()
    my_list = []
    for i in range(0, 40000):
        my_list.append(i)
    pr.disable()

    stats: pstats.Stats = pstats.Stats(pr)
    stats.sort_stats("tottime")
    # stats.sort_stats('cumulative')
    # stats.sort_stats('ncalls')
    # stats.sort_stats('pcalls')
    stats.print_stats(100)

    return None


if __name__ == "__main__":
    main()

# EOF
