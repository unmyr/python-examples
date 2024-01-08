# -*- coding: utf-8 -*-
"""Example of statement timeout."""
import logging
import os
import sys
import time
import traceback
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
logger = logging.getLogger(__name__)


def select_all(engine: sqlalchemy.engine.base.Engine) -> typing.Optional[typing.List[typing.Tuple]]:
    """Run main."""
    try:
        with engine.connect() as connection:
            result = connection.execute(sqlalchemy.text("SELECT pg_sleep(3)"))

        values: list = []
        for row in result:
            ary = [None] * len(row)
            for i, cell in enumerate(row):
                ary[i] = cell
            values.append(tuple(ary))

        return values

    except sqlalchemy.exc.ProgrammingError as exc:
        print(traceback.format_exc())
        print(exc)

    return None


def optional_int(num_str: typing.Optional[str]) -> typing.Optional[int]:
    """Optional[str] to Optional[int]."""
    if num_str is None:
        return None
    return int(num_str)


def main(driver_name: str) -> None:
    """Run main."""
    stream_handler: logging.StreamHandler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_formatter = logging.Formatter("[%(asctime)s] %(funcName)s - %(levelname)s - %(message)s")
    stream_handler.setFormatter(stream_formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    logger.propagate = False

    application_name = os.path.basename(__file__)
    engine: typing.Optional[sqlalchemy.engine.base.Engine] = None
    wait_sec: int = 4
    t_0: float
    try:
        database_url = sqlalchemy.engine.URL.create(
            driver_name,
            host=os.environ.get("PGHOST"),
            port=optional_int(os.environ.get("PGPORT")),
            database=os.environ.get("PGDATABASE"),
            username=os.environ.get("PGUSER"),
            password=os.environ.get("PGPASSWORD"),
        )
        if driver_name == "postgresql+psycopg2":
            engine = sqlalchemy.create_engine(
                database_url,
                connect_args={
                    "application_name": application_name,
                    "connect_timeout": 5,
                    "options": f"-c statement_timeout={wait_sec * 1000}",
                },
            )
        else:
            engine = sqlalchemy.create_engine(
                database_url,
                connect_args={"application_name": application_name, "timeout": wait_sec},
            )
        t_0 = time.time()
        val = select_all(engine)
        logger.info(__(f"val={val}"))
        t_1 = time.time()
        logger.info(__(f"dt={t_1 - t_0:.3}"))

    except (
        sqlalchemy.exc.ProgrammingError,
        sqlalchemy.exc.InterfaceError,
        sqlalchemy.exc.OperationalError,
    ) as exc:
        # pylint: disable=line-too-long
        # psycopg2
        #
        # * Connection timed out
        #   sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) timeout expired
        # * too many connections
        #   sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) FATAL:  too many connections for database "fruits"
        # * statement timeout
        #   sqlalchemy.exc.OperationalError: (psycopg2.errors.QueryCanceled) canceling statement due to statement timeout
        #
        # pg8000
        # * Connection timed out
        #   sqlalchemy.exc.InterfaceError: (pg8000.exceptions.InterfaceError) network error on read
        # * too many connections
        #   sqlalchemy.exc.ProgrammingError: (pg8000.dbapi.ProgrammingError) {'S': 'FATAL', 'V': 'FATAL', 'C': '53300', 'M': 'too many connections for database "fruits"', 'F': 'postinit.c', 'L': '364', 'R': 'CheckMyDatabase'}
        # * statement timeout
        #   sqlalchemy.exc.InterfaceError: (pg8000.exceptions.InterfaceError) network error on read
        #
        t_1 = time.time()
        logger.info(__(f"dt={t_1 - t_0:.3}"))
        logger.info(__(f"{type(exc)}"))
        logger.exception(exc)

    finally:
        if engine:
            engine.dispose()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] in ["postgresql+pg8000", "postgresql+psycopg2"]:
            main(sys.argv[1])
    else:
        print(f"usage: {sys.argv[0]} " "{postgresql+pg8000|postgresql+psycopg2}", file=sys.stderr)

# EOF
