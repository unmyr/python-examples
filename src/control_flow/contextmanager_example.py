# -*- coding: utf-8 -*-
"""With statement in Python."""
import io
import os
import traceback
import typing
from logging import getLogger, StreamHandler, DEBUG, Formatter
from contextlib import contextmanager


logger = getLogger(__name__)
stream_handler = StreamHandler()
stream_handler.setLevel(DEBUG)
stream_handler.setFormatter(Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.setLevel(DEBUG)
logger.addHandler(stream_handler)
logger.propagate = False


def get_fd_num() -> int:
    """Get file descripter."""
    return len(os.listdir(f"/proc/{os.getpid()}/fd"))


@contextmanager
def my_writer(
    file_name: str, open_mode: str = "w"
) -> typing.Generator[typing.IO, None, None]:
    """Simple file reader/writer"""
    logger.info(f"{file_name}: __enter__: num-fds={get_fd_num()}")
    with open(file_name, open_mode) as file_handle:
        logger.info(f"{file_name}: yield: num-fds={get_fd_num()}")
        yield file_handle
    logger.info(f"{file_name}: __exit__: num-fds={get_fd_num()}")


def main():
    """Run main."""
    try:
        out_file = "foo.log"
        with my_writer(out_file, "w") as file_handle:
            file_handle.write("This is a pen.")
        print("----")
        with my_writer("foo.log", "r") as file_handle:
            file_handle.write("data")

    except io.UnsupportedOperation as exc:
        logger.error(f"main(): {type(exc)}: num-fds={get_fd_num()}")
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
