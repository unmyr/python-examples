"""Example of logger."""
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
assert logger.level == logging.DEBUG

# pylint: disable=logging-too-many-args
print("\n[ WARNING/ERROR/CRITICAL log levels are displayed. ]")
logger.debug("%d: debug message", 1)  # NG
logger.info("%d: info message", 1)  # NG
logger.warning("%d: warn message", 1)
logger.error("%d: error message", 1)
logger.critical("%d: critical message", 1)

assert len(logger.handlers) == 0

print("\n[ All log levels are displayed. ]")
handler = logging.StreamHandler()
logger.addHandler(handler)
assert handler.level == logging.NOTSET

logger.debug("%d: debug message", 2)
logger.info("%d: info message", 2)
logger.warning("%d: warn message", 2)
logger.error("%d: error message", 2)
logger.critical("%d: critical message", 2)

print("\n[ Remove the added handler. ]")
logger.removeHandler(handler)
logger.debug("%d: debug message", 3)
logger.info("%d: info message", 3)
logger.warning("%d: warn message", 3)
logger.error("%d: error message", 3)
logger.critical("%d: critical message", 3)
