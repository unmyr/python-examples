# -*- coding: utf-8 -*-
"""Example of QueuePool."""
import os
import sys
import time
import typing
from contextlib import contextmanager

import sqlalchemy


def optional_int(num_str: typing.Optional[str]) -> typing.Optional[int]:
    """Optional[str] to Optional[int]."""
    if num_str is None:
        return None
    return int(num_str)


@contextmanager
def create_engine(driver_name: str) -> typing.Generator[sqlalchemy.engine.base.Engine, None, None]:
    """Create engine."""
    engine: sqlalchemy.engine.base.Engine = sqlalchemy.create_engine(
        sqlalchemy.engine.URL.create(
            driver_name,
            host=os.environ.get("PGHOST"),
            port=optional_int(os.environ.get("PGPORT")),
            database=os.environ.get("PGDATABASE"),
            username=os.environ.get("PGUSER"),
            password=os.environ.get("PGPASSWORD"),
        ),
        pool_size=1,
        max_overflow=1,
    )
    yield engine
    engine.dispose()


def main(driver_name: str) -> None:
    """Run main."""
    with create_engine(driver_name) as engine:
        t_0: float = time.time()
        for _ in range(1000):
            with engine.connect():
                pass
        t_1: float = time.time()
        print(f"dt = {(t_1 - t_0):.3f}s")


if __name__ == "__main__":
    if sys.argv[1] in ["postgresql+pg8000", "postgresql+psycopg2"]:
        main(sys.argv[1])
    else:
        print(f"usage: {sys.argv[0]} " "{postgresql+pg8000|postgresql+psycopg2}", file=sys.stderr)

# EOF
