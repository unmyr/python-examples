"""Example of logger."""
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

# pylint: disable=logging-too-many-args
logger.debug("%d: debug message", 1)
logger.info("%d: info message", 1)
logger.warning("%d: warn message", 1)
logger.error("%d: error message", 1)
logger.critical("%d: critical message", 1)
