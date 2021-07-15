"""Example of a ThreadPoolExecuter."""
from concurrent.futures import ThreadPoolExecutor
from logging import getLogger, StreamHandler, DEBUG, Formatter
import concurrent.futures
import functools
import time
import typing

pool: typing.Optional[ThreadPoolExecutor] = None


class BraceMessage:
    """Brace message"""
    def __init__(self, fmt, *args, **kwargs) -> typing.NoReturn:
        self.fmt = fmt
        self.args = args
        self.kwargs = kwargs

    def __str__(self) -> str:
        return self.fmt.format(*self.args, **self.kwargs)


__ = BraceMessage
logger = getLogger(__name__)


def delay_hello(msg: str, waitSec: int) -> str:
    """Delay hello"""
    logger.debug(__('BEGIN: {}', msg))
    time.sleep(waitSec)
    logger.debug(__('END: {}', msg))
    return f"Hello {msg}"


def my_decorator(func: callable) -> callable:
    """My decorator."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # pylint: disable=global-statement
        global pool
        try:
            logger.info(__('CALL: wrapper()'))
            ret = func(*args, **kwargs)
            logger.info(__('DONE: wrapper(): ret={}', ret))
        finally:
            logger.info(__('CALL: pool.shutdown()'))
            # pool.shutdown()
            # pool.shutdown(wait=True)
            pool.shutdown(wait=False)
            logger.info(__('DONE: pool.shutdown()'))

    return wrapper


@my_decorator
def run(timeout) -> bool:
    """Run tasks"""
    # pylint: disable=global-statement
    global pool
    pool = ThreadPoolExecutor(2)

    params: typing.List[typing.Tuple[str, int]] = [
        ('foo', 2), ('bar', 6), ('baz', 10)
    ]

    futures: typing.List[concurrent.futures.Future] = []
    for param in params:
        futures.append(pool.submit(delay_hello, *param))

    for future in futures:
        try:
            logger.info(__('CALL: future.result(timeout={})', timeout))
            val = future.result(timeout=timeout)
            logger.info(__('DONE: future.result(timeout={}): {}', timeout, val))
        except concurrent.futures.TimeoutError:
            # logger.exception(exc)
            logger.warning(__('FAIL: future.result(timeout={}): timed out', timeout))
    return True


def main() -> typing.NoReturn:
    """Run main."""
    stream_handler = StreamHandler()
    stream_handler.setLevel(DEBUG)
    stream_formatter = Formatter(
        '[%(asctime)s] %(levelname)s - %(funcName)s - %(message)s'
    )
    stream_handler.setFormatter(stream_formatter)
    logger.setLevel(DEBUG)
    logger.addHandler(stream_handler)
    logger.propagate = False
    logger.info(__('CALL: run(2)'))
    ret = run(2)
    logger.info(__('DONE: run(2): ret={}', ret))


if __name__ == '__main__':
    main()

# EOF
