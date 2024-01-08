# -*- coding: utf-8 -*-
"""Example of statement timeout."""
import logging
import os
import time
import traceback
import typing
from logging import DEBUG, Formatter, StreamHandler, getLogger

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
logger: logging.Logger = getLogger(__name__)


def select_all(engine: sqlalchemy.engine.base.Engine) -> typing.Optional[typing.List[typing.Tuple]]:
    """Run main."""
    try:
        with engine.connect() as connection:
            result = connection.execute(
                sqlalchemy.text(
                    "SELECT pid, datname, usename, application_name, state, backend_type"
                    " FROM pg_stat_activity"
                )
            )

        values: list = []
        for row in result:
            ary = [None] * len(row)
            for i, cell in enumerate(row):
                ary[i] = cell
            values.append(tuple(ary))
            print(row)

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
    stream_handler: logging.StreamHandler = StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_formatter: logging.Formatter = Formatter(
        "[%(asctime)s] %(funcName)s - %(levelname)s - %(message)s"
    )
    stream_handler.setFormatter(stream_formatter)
    logger.setLevel(DEBUG)
    logger.addHandler(stream_handler)
    logger.propagate = False

    application_name: str = os.path.basename(__file__)
    engine: typing.Optional[sqlalchemy.engine.base.Engine] = None
    wait_sec: int = 4
    try:
        database_url = sqlalchemy.engine.URL.create(
            driver_name,
            host=os.environ.get("PGHOST"),
            port=optional_int(os.environ.get("PGPORT")),
            database=os.environ.get("PGDATABASE"),
            username=os.environ.get("PGUSER"),
            password=os.environ.get("PGPASSWORD"),
        )

        connect_args: dict
        if driver_name == "postgresql+psycopg2":
            connect_args = {
                "application_name": application_name,
                "connect_timeout": 5,
                "options": f"-c statement_timeout={wait_sec * 1000}",
            }
        elif driver_name == "postgresql+pg8000":
            connect_args = {"application_name": application_name, "timeout": wait_sec}

        engine = sqlalchemy.create_engine(database_url, connect_args=connect_args)
        t_0 = time.time()
        val = select_all(engine)
        logger.debug(__(f"val={val}"))
        t_1 = time.time()
        logger.debug(__(f"dt={t_1 - t_0:.3}"))

    except (
        sqlalchemy.exc.ProgrammingError,
        sqlalchemy.exc.InterfaceError,
        sqlalchemy.exc.OperationalError,
    ) as exc:
        logger.info(__(f"{type(exc)}"))
        logger.exception(exc)

    finally:
        if engine:
            engine.dispose()


if __name__ == "__main__":
    main("postgresql+psycopg2")

# EOF
