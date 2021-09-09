"""Example of logger."""
import logging
import sys
import traceback

try:
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False

    logger.debug("DEBUG: hello world!")
    logger.info("INFO: hello world!")
    logger.error("ERROR: hello world!")
    logger.fatal("FATAL: hello world!")

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
