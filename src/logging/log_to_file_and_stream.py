"""Example of logger."""
from logging import getLogger, StreamHandler, FileHandler, DEBUG, Formatter


logger = getLogger(__name__)


def main():
    """Run main."""
    logger.debug("hello world!")


if __name__ == '__main__':
    stream_handler = StreamHandler()
    stream_handler.setLevel(DEBUG)
    file_handler = FileHandler('log_to_file_and_stream', 'a')
    file_handler.setLevel(DEBUG)
    file_formatter = Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)

    logger.setLevel(DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.propagate = False
    main()

# EOF
