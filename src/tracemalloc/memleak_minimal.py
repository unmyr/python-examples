"""Example of tracemalloc."""
# ruff: noqa: F841
import tracemalloc


def main():
    """Run main."""
    tracemalloc.start()

    snapshot1: tracemalloc.Snapshot = tracemalloc.take_snapshot()

    my_array = [None] * 1024  # pylint: disable=unused-variable
    # del my_array

    snapshot2 = tracemalloc.take_snapshot()
    top_stats = snapshot2.compare_to(snapshot1, "lineno")

    print("[ Top 10 ]")
    for stat in top_stats[:10]:
        print(stat)

    tracemalloc.stop()


if __name__ == "__main__":
    main()

# EOF
