"""Example of a ThreadPoolExecuter."""
from concurrent.futures import ThreadPoolExecutor
from logging import getLogger, StreamHandler, DEBUG, Formatter
import concurrent.futures
import time
import typing


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


def run(timeout: int) -> bool:
    """Run tasks"""
    pool: ThreadPoolExecutor = ThreadPoolExecutor(2)
    print(f'type(pool)={type(pool)}')
    futures: typing.List[concurrent.futures.Future] = []
    params: typing.List[typing.Tuple[str, int]] = [
        ('foo', 3), ('bar', 1), ('baz', 1)
    ]
    for param in params:
        futures.append(pool.submit(delay_hello, *param))

    for i, future in enumerate(futures):
        try:
            logger.info(__('CALL: result(timeout={}): {}', timeout, params[i]))
            val = future.result(timeout=timeout)
            logger.info(__('DONE: result(timeout={}): {}: ret=\"{}\"', timeout, params[i], val))
        except concurrent.futures.TimeoutError:
            # logger.exception(exc)
            logger.warning(__('FAIL: result(timeout={}): {}: timed out', timeout, params[i]))

    logger.info(__('CALL: pool.shutdown()'))
    pool.shutdown()
    logger.info(__('DONE: pool.shutdown()'))

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
