"""Example of logger."""
from logging import getLogger, StreamHandler, DEBUG
import sys
import traceback

try:
    logger = getLogger(__name__)
    handler = StreamHandler()
    handler.setLevel(DEBUG)
    logger.setLevel(DEBUG)
    logger.addHandler(handler)
    logger.propagate = False

    logger.debug("hello world!")

except TypeError as exc:
    print(f"{exc.args}", file=sys.stderr)
    for attr_name in dir(exc):
        try:
            if hasattr(exc, attr_name):
                attr_obj = getattr(exc, attr_name)
                print(f"attr={attr_name}, type={type(attr_obj)}, callable={callable(attr_obj)}")
            else:
                print(f"attr={attr_name}")

        except AttributeError as exc2:
            print(type(exc2))
            print(traceback.format_exc())
            print(f"attr={attr_name}")
