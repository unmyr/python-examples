"""Example of NullPool."""
from contextlib import contextmanager
import os
import sys
import time
import typing

import sqlalchemy


def optional_int(
    num_str: typing.Optional[str]
) -> typing.Optional[int]:
    """Optional[str] to Optional[int]."""
    if num_str is None:
        return None
    return int(num_str)


@contextmanager
def create_engine(
    driver_name: str
) -> typing.Generator[sqlalchemy.engine.base.Engine, None, None]:
    """Create engine."""
    config: typing.Dict
    if driver_name == 'sqlite':
        db_uri = sqlalchemy.engine.URL.create(
            drivername=driver_name,
            host='',
            port=None,
            database=':memory:',
            username='',
            password=''
        )
        config = dict()
    else:
        db_uri = sqlalchemy.engine.URL.create(
            drivername=driver_name,
            host=os.environ.get('PGHOST'),
            port=typing.cast(int, os.environ.get('PGPORT')),
            database=os.environ.get('PGDATABASE'),
            username=os.environ.get('PGUSER'),
            password=os.environ.get('PGPASSWORD')
        )
        config = dict(
            pool_size=1,
            max_overflow=1
        )

    engine = sqlalchemy.create_engine(
        db_uri,
        **config,
        echo=False
    )
    if driver_name == 'sqlite':
        with engine.connect() as conn:
            conn.execute(
                sqlalchemy.text("ATTACH DATABASE ':memory:' AS :schema"),
                schema='guest'
            )
    yield engine
    engine.dispose()


def main(driver_name: str) -> None:
    """Run main."""
    with create_engine(driver_name) as engine:
        t_0 = time.time()
        for _ in range(1000):
            with engine.connect():
                pass
        t_1 = time.time()
        print(f'dt = {(t_1 - t_0):.3f}s')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main('sqlite')
    elif len(sys.argv) == 2 and sys.argv[1] in [
            'sqlite', 'postgresql+pg8000', 'postgresql+psycopg2'
    ]:
        main(sys.argv[1])
    else:
        print(
            f"usage: {sys.argv[0]} "
            '{sqlite|postgresql+pg8000|postgresql+psycopg2}',
            file=sys.stderr
        )

# EOF
