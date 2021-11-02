# -*- coding: utf-8 -*-
"""Example of parallel execution."""
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import logging
import os
import sys
import time
import typing

import sqlalchemy


class BraceMessage:
    """Brace message"""
    def __init__(self, fmt, *args, **kwargs) -> None:
        self.fmt = fmt
        self.args = args
        self.kwargs = kwargs

    def __str__(self) -> str:
        return self.fmt.format(*self.args, **self.kwargs)


__ = BraceMessage
logger: logging.Logger = logging.getLogger(__name__)


def optional_int(
    num_str: typing.Optional[str]
) -> typing.Optional[int]:
    """Optional[str] to Optional[int]."""
    if num_str is None:
        return None
    return int(num_str)


class EngineHelper:
    """Engine helper."""
    def __init__(
        self, driver_name: str,
        application_name: str,
        poolclass=sqlalchemy.pool.QueuePool
    ) -> None:
        database_url = sqlalchemy.engine.URL.create(
            driver_name,
            host=os.environ.get('PGHOST'),
            port=optional_int(os.environ.get('PGPORT')),
            database=os.environ.get('PGDATABASE'),
            username=os.environ.get('PGUSER'),
            password=os.environ.get('PGPASSWORD')
        )
        logger.debug(__(f'CALL: create_engine({driver_name})'))
        self.engine: sqlalchemy.engine.base.Engine = sqlalchemy.create_engine(
            database_url,
            poolclass=poolclass,
            connect_args={
                'application_name': application_name
            }
        )
        logger.debug(__(f'DONE: create_engine: {type(self.engine)}'))

    def __del__(self) -> None:
        logger.debug('CALL: engine.dispose()')
        self.engine.dispose()
        logger.debug('DONE: engine.dispose()')


def execute_select(
    cnt: int,
    engine: sqlalchemy.engine.base.Engine,
    application_name: str
) -> typing.List[typing.Tuple]:
    """Delay hello"""
    with engine.connect() as conn:
        logger.debug(__(f'CALL: {cnt}: conn.execute'))
        result = conn.execute(
            sqlalchemy.text(
                f"SELECT pg_sleep(2), {cnt}"
            ),
            {'application_name': application_name}
        )
        logger.debug(__(f'DONE: {cnt}: conn.execute'))

    values = []
    for row in result:
        ary = [None] * len(row)
        for i, cell in enumerate(row):
            ary[i] = cell
        values.append(tuple(ary))
    return values


def call_engine_helper(
    driver_name: str,
    application_name: str,
    poolclass: typing.Union[typing.Type[sqlalchemy.pool.QueuePool],
                            typing.Type[sqlalchemy.pool.StaticPool]]
) -> None:
    """Call engine helper"""
    total_tasks: int = 30
    parallel: int = 5
    pool: ThreadPoolExecutor = ThreadPoolExecutor(parallel)
    try:
        futures: typing.List[concurrent.futures.Future] = []

        engine_helper = EngineHelper(driver_name, application_name, poolclass)
        params = [(engine_helper.engine, application_name)] * total_tasks
        for i, param in enumerate(params):
            futures.append(pool.submit(execute_select, i, *param))
        for future in futures:
            val = future.result(timeout=3)
            logger.debug(__('val: {}', val))
    except concurrent.futures.TimeoutError as exc:
        logger.info(__(f'WARN: {type(exc)}'))

    finally:
        logger.info(__('CALL: pool.shutdown()'))
        pool.shutdown()
        logger.info(__('DONE: pool.shutdown()'))


def main(driver_name: str, pool_name: str) -> None:
    """Run main."""
    stream_handler: logging.StreamHandler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_formatter: logging.Formatter = logging.Formatter(
        '[%(asctime)s] %(funcName)s - %(levelname)s - %(message)s'
    )
    stream_handler.setFormatter(stream_formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    logger.propagate = False

    application_name = os.path.basename(__file__)

    t_0: float = time.time()
    poolclass: typing.Union[typing.Type[sqlalchemy.pool.QueuePool],
                            typing.Type[sqlalchemy.pool.StaticPool]]
    if pool_name == 'StaticPool':
        poolclass = sqlalchemy.pool.StaticPool
    elif pool_name == 'QueuePool':
        poolclass = sqlalchemy.pool.QueuePool

    call_engine_helper(driver_name, application_name, poolclass)
    t_1: float = time.time()
    logger.info(__(f'dt={t_1 - t_0:.3}'))


if __name__ == '__main__':
    if len(sys.argv) == 3:
        if (sys.argv[1] in ['postgresql+pg8000', 'postgresql+psycopg2']
                and sys.argv[2] in ['StaticPool', 'QueuePool']):
            main(sys.argv[1], sys.argv[2])
    else:
        print(
            f"usage: {sys.argv[0]} "
            '{postgresql+pg8000|postgresql+psycopg2} {StaticPool|QueuePool}',
            file=sys.stderr
        )

# EOF
