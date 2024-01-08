# -*- coding: utf-8 -*-
"""Example of QueuePool pool timeout."""
import logging
import os
import sys
import time
import typing
from contextlib import contextmanager

import sqlalchemy


class BraceMessage:
    """Brace message"""

    def __init__(self, fmt: str, *args: typing.Tuple, **kwargs: dict) -> None:
        self.fmt = fmt
        self.args = args
        self.kwargs = kwargs

    def __str__(self) -> str:
        return self.fmt.format(*self.args, **self.kwargs)


__ = BraceMessage
logger: logging.Logger = logging.getLogger(__name__)
stream_handler: logging.StreamHandler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.propagate = False
stream_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))


def optional_int(num_str: typing.Optional[str]) -> typing.Optional[int]:
    """Optional[str] to Optional[int]."""
    if num_str is None:
        return None
    return int(num_str)


@contextmanager
def create_engine(driver_name: str) -> typing.Generator[sqlalchemy.engine.base.Engine, None, None]:
    """Create engine."""
    database_url: sqlalchemy.engine.URL
    if driver_name.startswith("postgresql+"):
        database_url = sqlalchemy.engine.URL.create(
            driver_name,
            host=os.environ.get("PGHOST"),
            port=optional_int(os.environ.get("PGPORT")),
            database=os.environ.get("PGDATABASE"),
            username=os.environ.get("PGUSER"),
            password=os.environ.get("PGPASSWORD"),
        )
    elif driver_name == "sqlite":
        database_url = sqlalchemy.engine.URL.create(
            driver_name,
            host="",
            port=None,
            database=os.environ.get(":memory:"),
            username="",
            password="",
        )

    engine: sqlalchemy.engine.base.Engine
    if driver_name.startswith("postgresql+"):
        engine = sqlalchemy.create_engine(database_url, pool_size=1, max_overflow=0, pool_timeout=3)
    elif driver_name == "sqlite":
        # TypeError: Invalid argument(s) 'max_overflow','pool_timeout' sent to create_engine(),
        # using configuration SQLiteDialect_pysqlite/SingletonThreadPool/Engine.
        # Please check that the keyword arguments are appropriate for this combination of components.
        engine = sqlalchemy.create_engine(
            database_url, poolclass=sqlalchemy.pool.SingletonThreadPool, pool_size=1
        )

    yield engine
    engine.dispose()


def setup_sqlite_table(engine: sqlalchemy.engine.base.Engine):
    """Setup sqlite table."""
    try:
        with engine.connect() as connection:
            connection.execute(
                sqlalchemy.text("ATTACH DATABASE ':memory:' AS :schema"), {"schema": "guest"}
            )

            # SQLite3 serial type wasn't incremented
            # all of the id element was None
            connection.execute(
                sqlalchemy.text(
                    "CREATE TABLE guest.fruits_menu ("
                    "  id INTEGER PRIMARY KEY,"
                    "  name VARCHAR(16) UNIQUE,"
                    "  price INTEGER,"
                    "  mod_time timestamp DEFAULT current_timestamp"
                    ")"
                )
            )

            fruit_item_list: typing.List[dict] = [
                {"name": "Apple", "price": 100},
                {"name": "Banana", "price": 120},
                {"name": "Orange", "price": 110},
                {"name": "リンゴ", "price": 180},
            ]
            connection.execute(
                sqlalchemy.text("INSERT INTO fruits_menu (name, price) VALUES (:name, :price)"),
                fruit_item_list,
            )
    except sqlalchemy.exc.ProgrammingError as exc:
        logger.exception(exc)


def main(driver_name: str) -> None:
    """Run main."""
    try:
        logger.info(__(f"create_engine({driver_name})"))
        with create_engine(driver_name) as engine:
            logger.info("BEGIN connect")
            if driver_name == "sqlite":
                setup_sqlite_table(engine)

            t_0: float = time.time()
            with engine.connect() as conn1, engine.connect() as conn2:
                result = conn1.execute(sqlalchemy.text("SELECT * FROM guest.fruits_menu"))
                values: list = []
                for row in result:
                    ary = [None] * len(row)
                    for i, cell in enumerate(row):
                        ary[i] = cell
                    values.append(tuple(ary))
                logger.info(values)

                time.sleep(5)
                result = conn2.execute(sqlalchemy.text("SELECT * FROM guest.fruits_menu"))

                for row in result:
                    ary = [None] * len(row)
                    for i, cell in enumerate(row):
                        ary[i] = cell
                    values.append(tuple(ary))
                logger.info(values)

            t_1: float = time.time()
            logger.info(f"dt = {(t_1 - t_0):.3f}s")

    except sqlalchemy.exc.TimeoutError as exc:
        logger.exception(exc)

    finally:
        logger.info("END connect")


if __name__ == "__main__":
    if sys.argv[1] in ["postgresql+pg8000", "postgresql+psycopg2", "postgresql+pygresql", "sqlite"]:
        main(sys.argv[1])
    else:
        print(
            f"usage: {sys.argv[0]} " "{postgresql+pg8000|postgresql+psycopg2|postgresql+pygresql}",
            file=sys.stderr,
        )

# EOF
