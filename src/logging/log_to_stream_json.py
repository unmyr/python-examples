"""Example of logger."""
from datetime import datetime
import json
import logging
import math


class Hello:
    """Hello class"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'Hello {self.message}'


def dict_to_serialize(obj):
    """Serialize datetime"""
    if isinstance(obj, (datetime)):
        return obj.isoformat(timespec='seconds')
    elif isinstance(obj, (Hello)):
        return str(obj)
    else:
        raise TypeError(f'Type {type(obj)} not serializable')


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.propagate = False

dict_not_serializable = {
    'bool': True,
    'class': Hello('world'),
    'datetime': datetime.now(),
    'null': None,
    'numbers': {'integer': -1, 'pi': math.pi, 'nan': float('nan'), 'inf': float('inf'), '-inf': float('-inf')},
    'str': 'foo',
    'tuple': ('Hello', 'world')
}
logger.info(json.dumps(dict_not_serializable, default=dict_to_serialize, indent=2))

logger.removeHandler(handler)
