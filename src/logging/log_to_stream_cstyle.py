"""Example of logger."""
import datetime
import math
from logging import DEBUG, StreamHandler, getLogger

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

# pylint: disable=logging-too-many-args
logger.debug(
    "number=%s pi=%s dict=%s",
    1,
    "{:1.2f}".format(math.pi),
    {"key1": True, "key2": datetime.datetime.now()},
)

logger.removeHandler(handler)
