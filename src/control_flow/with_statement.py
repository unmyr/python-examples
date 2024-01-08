# -*- coding: utf-8 -*-
"""With statement in Python."""
import io
import traceback
from logging import DEBUG, Formatter, StreamHandler, getLogger

logger = getLogger(__name__)
stream_handler = StreamHandler()
stream_handler.setLevel(DEBUG)
stream_handler.setFormatter(Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.setLevel(DEBUG)
logger.addHandler(stream_handler)
logger.propagate = False


class MyWriter:
    """Simple file reader/writer"""

    def __init__(self, file_name: str, mode: str = "w"):
        self.file_name = file_name
        self.open_mode = mode
        self.file_handle = None

    def __enter__(self):
        logger.info(f"{self.file_name}: __enter__: open file")
        self.file_handle = open(self.file_name, self.open_mode)
        return self.file_handle

    def __exit__(self, exc_type, exc_value, traceback_):
        if exc_type is None:
            logger.info(f"{self.file_name},: __exit__: ")
        else:
            logger.error(
                f"{self.file_name},: __exit__: "
                f"exc_type={exc_type},"
                f"exc_value={exc_value}, "
                f"traceback={type(traceback_)}"
            )
        if self.file_handle is not None:
            self.file_handle.close()
            logger.info(f"{self.file_name}: __exit__: close file")


def main():
    """Run main."""
    try:
        out_file = "foo.log"
        with MyWriter(out_file, "w") as file_handle:
            file_handle.write("This is a pen.")
        print("----")
        with MyWriter("foo.log", "r") as file_handle:
            file_handle.write("data")

    except io.UnsupportedOperation as exc:
        logger.error(f"main(): {type(exc)}")
        logger.error(
            f"main(): args={exc.args} "
            f"errno={exc.errno} "
            f"filename={exc.filename} "
            f"filename2={exc.filename2} "
            f"strerror={exc.strerror} "
        )
        logger.error(traceback.format_exc())


if __name__ == "__main__":
    main()

# EOF
