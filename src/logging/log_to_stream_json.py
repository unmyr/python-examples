"""Example of logger."""
from logging import getLogger, StreamHandler, DEBUG
import json


logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

logger.debug(
    json.dumps(
        {
            'key1': 'value1',
            'key2': 'value2'
        }
    )
)
