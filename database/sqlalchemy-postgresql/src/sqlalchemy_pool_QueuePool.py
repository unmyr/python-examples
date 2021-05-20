# -*- coding: utf-8 -*-
"""Example of QueuePool."""
from contextlib import contextmanager
import os
import sys
import time

import sqlalchemy


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
        max_overflow=1
    )
    yield engine
    engine.dispose()


def main(driver_name: str):
    """Run main."""
    with create_engine(driver_name) as engine:
        t_0 = time.time()
        for _ in range(1000):
            with engine.connect():
                pass
        t_1 = time.time()
        print(f'dt = {(t_1 - t_0):.3f}s')


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
