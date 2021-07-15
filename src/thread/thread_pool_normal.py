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


def delay_hello(msg: str) -> str:
    """Delay hello"""
    logger.debug(__('BEGIN: {}', msg))
    time.sleep(2)
    logger.debug(__('END: {}', msg))
    return f"Hello {msg}"


def run(timeout: int) -> bool:
    """Run tasks"""
    pool: ThreadPoolExecutor = ThreadPoolExecutor(2)
    print(f'type(pool)={type(pool)}')
    futures: typing.List[concurrent.futures.Future] = []

    params: typing.List[str] = ['foo', 'bar', 'baz']
    for param in params:
        futures.append(pool.submit(delay_hello, param))
    logger.info(__(f'type(futures[0])={type(futures[0])}'))

    for future in futures:
        try:
            logger.info(__('CALL: future.result(timeout={})', timeout))
            val = future.result(timeout=timeout)
            logger.info(__('DONE: future.result(timeout={}): {}', timeout, val))
        except concurrent.futures.TimeoutError:
            # logger.exception(exc)
            logger.warning(__('FAIL: future.result(timeout={}): timed out', timeout))

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
    ret = run(3)
    logger.info(__('DONE: run(2): ret={}', ret))


if __name__ == '__main__':
    main()

# EOF
