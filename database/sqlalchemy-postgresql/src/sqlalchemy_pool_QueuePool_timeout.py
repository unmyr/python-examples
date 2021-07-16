# -*- coding: utf-8 -*-
"""Example of QueuePool pool timeout."""
from contextlib import contextmanager
import logging
import os
import sys
import time
import traceback
import typing

import sqlalchemy


logger: logging.Logger = logging.getLogger(__name__)
stream_handler: logging.StreamHandler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.propagate = False
stream_handler.setFormatter(
    logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
)


@contextmanager
def create_engine(driver_name: str) -> typing.NoReturn:
    """Create engine."""
    engine: sqlalchemy.engine.base.Engine = sqlalchemy.create_engine(
        sqlalchemy.engine.URL.create(
            driver_name,
            host=os.environ.get('PGHOST'),
            port=os.environ.get('PGPORT'),
            database=os.environ.get('PGDATABASE'),
            username=os.environ.get('PGUSER'),
            password=os.environ.get('PGPASSWORD')
        ),
        pool_size=1,
        max_overflow=0,
        pool_timeout=3
    )
    yield engine
    engine.dispose()


def main(driver_name: str) -> typing.NoReturn:
    """Run main."""
    try:
        with create_engine(driver_name) as engine:
            logger.info('BEGIN connect')
            t_0: float = time.time()
            with engine.connect() as conn1, engine.connect() as conn2:
                result = conn1.execute(
                    sqlalchemy.text("SELECT * FROM guest.fruits_menu")
                )
                logger.info(result)
                time.sleep(5)
                result = conn2.execute(
                    sqlalchemy.text("SELECT * FROM guest.fruits_menu")
                )
                logger.info(result)
            t_1: float = time.time()
            logger.info(f'dt = {(t_1 - t_0):.3f}s')

    except sqlalchemy.exc.TimeoutError as exc:
        logger.error(traceback.format_exc())
        logger.error(exc)

    finally:
        logger.info('END connect')


if __name__ == '__main__':
    if sys.argv[1] in ['postgresql+pg8000', 'postgresql+psycopg2']:
        main(sys.argv[1])
    else:
        print(
            f"usage: {sys.argv[0]} "
            '{postgresql+pg8000|postgresql+psycopg2}',
            file=sys.stderr
        )

# EOF
