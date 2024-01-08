"""Example of logger."""
import datetime
import math
from logging import DEBUG, StreamHandler, getLogger


class BraceMessage:
    """Brace message"""

    def __init__(self, fmt, *args, **kwargs):
        self.fmt = fmt
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return self.fmt.format(*self.args, **self.kwargs)


__ = BraceMessage

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

logger.debug(
    __(
        "number={} pi={:1.2f} dict={}",
        1,
        math.pi,
        {"key1": True, "key2": datetime.datetime.now()},
    )
)
logger.removeHandler(handler)
