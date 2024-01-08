"""Example of logger."""
import logging
import time
import tracemalloc
from logging import getLogger
from logging.handlers import RotatingFileHandler


def app(logger: logging.Logger):
    """Run app."""

    class FooFilter(logging.Filter):
        """Remove foo."""

        def filter(self, record: logging.LogRecord):
            """Filter settings."""
            return "foo" not in record.getMessage()

    logger.addFilter(FooFilter())
    for _ in range(16):
        logger.debug("INFO: hello world!")
        logger.debug("INFO: hello foo!")
        logger.debug("INFO: hello bar!")
        logger.debug("INFO: hello world!")
        logger.debug("INFO: hello foo!")
        logger.debug("INFO: hello bar!")
        logger.debug("INFO: hello world!")
        logger.debug("INFO: hello foo!")
        logger.debug("INFO: hello bar!")
        logger.debug("INFO: hello bar!")
    logger.info("INFO: hello world!")
    logger.info("INFO: hello foo!")


def main():
    """Run main."""
    step = 60
    total = step * 200
    durations = []

    tracemalloc.start()

    logger = getLogger(__name__)
    snapshot1 = tracemalloc.take_snapshot()

    rotate_handler = RotatingFileHandler(
        "log_to_file_rotate", "a", maxBytes=1024 * 2, backupCount=1
    )
    rotate_handler.setLevel(logging.INFO)
    logger.setLevel(logging.INFO)
    logger.addHandler(rotate_handler)

    logger.propagate = False

    for i in range(total):
        t_0 = time.time()
        app(logger)
        t_1 = time.time()
        durations.append(t_1 - t_0)
        if i % step == 0:
            print(
                "\ri={:6d}, {:3.1f} %, dt={:3.6f}".format(
                    i, 100 * i / total, t_1 - t_0
                ),
                end="",
            )
    print()

    logger.removeHandler(rotate_handler)

    snapshot2 = tracemalloc.take_snapshot()
    top_stats = snapshot2.compare_to(snapshot1, "lineno")

    print("[ Top 10 ]")
    for stat in top_stats[:10]:
        print(stat)

    with open("perf.csv", "w") as f:
        f.write("min,avg,max\n")
        for i in range(total):
            if i % step == (step - 1):
                sub_durations = durations[(i + 1 - step) : i + 1]
                min_val = min(sub_durations)
                avg_val = sum(sub_durations) / step
                max_val = max(sub_durations)

                f.write("{},{},{}\n".format(min_val, avg_val, max_val))


if __name__ == "__main__":
    main()
