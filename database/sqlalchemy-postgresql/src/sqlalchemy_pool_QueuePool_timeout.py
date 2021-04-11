# -*- coding: utf-8 -*-
"""Example of QueuePool pool timeout."""
from contextlib import contextmanager
from logging import getLogger, StreamHandler, DEBUG, Formatter
import os
import sys
import time
import traceback

import sqlalchemy


logger = getLogger(__name__)
stream_handler = StreamHandler()
stream_handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(stream_handler)
logger.propagate = False
stream_handler.setFormatter(
    Formatter('[%(asctime)s] %(levelname)s: %(message)s')
)


@contextmanager
def create_engine(driver_name: str):
    """Create engine."""
    engine = sqlalchemy.create_engine(
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


def main(driver_name: str):
    """Run main."""
    try:
        with create_engine(driver_name) as engine:
            logger.info('BEGIN connect')
            t_0 = time.time()
            with engine.connect() as conn1, engine.connect() as conn2:
                result = conn1.execute(
                    sqlalchemy.text("SELECT * FROM FruitsMenu")
                )
                logger.info(result)
                time.sleep(5)
                result = conn2.execute(
                    sqlalchemy.text("SELECT * FROM FruitsMenu")
                )
                logger.info(result)
            t_1 = time.time()
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
        print("usage: {sys.argv[0]} " + '{postgresql+pg8000|postgresql+psycopg2}', sys.stderr)

# EOF
