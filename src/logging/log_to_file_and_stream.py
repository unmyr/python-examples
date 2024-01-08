"""Example of logger."""
import logging
import tracemalloc
from logging import FileHandler, Formatter, StreamHandler, getLogger

logger = getLogger(__name__)


def app() -> None:
    """Run app."""
    logger.debug("This is a debug message.")
    logger.info("This is a info message.")
    logger.warning("This is a warn message.")
    logger.error("This is a error message.")
    logger.critical("This is a critical message.")


def main() -> None:
    """Run main."""
    stream_handler = StreamHandler()
    stream_handler.setLevel(logging.INFO)
    file_handler = FileHandler("log_to_file_and_stream", "a")
    file_handler.setLevel(logging.INFO)
    file_formatter = Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.propagate = False
    app()
    logger.removeHandler(stream_handler)
    logger.removeHandler(file_handler)


if __name__ == "__main__":
    tracemalloc.start()
    snapshot1 = tracemalloc.take_snapshot()
    for i in range(1):
        main()
    snapshot2 = tracemalloc.take_snapshot()
    top_stats = snapshot2.compare_to(snapshot1, "lineno")

    print("[ Top 10 ]")
    for stat in top_stats[:10]:
        print(stat)
    tracemalloc.stop()

# EOF
