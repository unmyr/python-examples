"""Example of logger."""
from logging import DEBUG, StreamHandler, getLogger
from logging.handlers import RotatingFileHandler

logger = getLogger(__name__)
stream_handler = StreamHandler()
stream_handler.setLevel(DEBUG)
rotate_handler = RotatingFileHandler(
    'log_to_file_rotate', 'a', maxBytes=2 * len("hello world 1"), backupCount=1
)
rotate_handler.setLevel(DEBUG)

logger.setLevel(DEBUG)
logger.addHandler(rotate_handler)
logger.addHandler(stream_handler)
logger.propagate = False

logger.debug("hello world 1")
logger.debug("hello world 2")
logger.debug("hello world 3")
logger.debug("hello world 4")

logger.removeHandler(stream_handler)
logger.removeHandler(rotate_handler)
