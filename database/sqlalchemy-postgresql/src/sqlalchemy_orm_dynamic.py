# -*- coding: utf-8 -*-
"""Example of execute SELECT."""
import json
import logging
import os
import sys
import time
import traceback
import typing
from contextlib import contextmanager

import sqlalchemy
import sqlalchemy.orm

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
def create_session(
    driver_name: str,
) -> typing.Generator[typing.Tuple[sqlalchemy.orm.Session, sqlalchemy.schema.MetaData], None, None]:
    """Create engine."""
    t_0: float = time.time()
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
    t_1: float = time.time()
    metadata = sqlalchemy.MetaData(engine)

    Session = sqlalchemy.orm.sessionmaker(engine)
    t_2: float = time.time()
    with engine.connect() as connection:
        t_3: float = time.time()
        logger.info("engine.connect()")
        t_4: float = time.time()
        with Session(bind=connection) as session:
            t_5: float = time.time()
            yield session, metadata
        logger.info("engine.close()")
    logger.info("engine.dispose()")
    t_6: float = time.time()
    engine.dispose()
    t_7: float = time.time()

    # pylint: disable=logging-too-many-args
    logger.info(
        (
            "perf: "
            "create_engine(): %.3fs, "
            "MetaData()+sessionmaker(): %.3fs, "
            "engine.connect(): %.3fs, "
            "Session(bind=connection): %.3fs, "
            "engine.dispose: %.3fs"
        ),
        t_1 - t_0,
        t_2 - t_1,
        t_3 - t_2,
        t_5 - t_4,
        t_7 - t_6,
    )


def execute_query(session, metadata) -> dict:
    """Execute query."""
    columns = (
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("name", sqlalchemy.String(length=16), unique=True),
        sqlalchemy.Column("price", sqlalchemy.Integer),
        sqlalchemy.Column("mod_time", sqlalchemy.DateTime),
    )
    fruit_item_table = sqlalchemy.Table("fruits_menu", metadata, *columns, {"schema": "guest"})

    class FruitsMenu(object):
        """OR Mapper for FRUITS_MENU table."""

    sqlalchemy.orm.mapper(FruitsMenu, fruit_item_table)

    # pylint: disable=no-member
    items = (
        session.query(FruitsMenu)
        .filter(
            sqlalchemy.or_(
                FruitsMenu.name == "Apple",  # type: ignore
                FruitsMenu.name == "Orange",  # type: ignore
            )
        )
        .all()
    )
    logger.info(f"Total: {len(items)} items.")

    records = []
    for item in items:
        logger.info(
            f"id={item.id} name='{item.name}' price={item.price} mod_time='{item.mod_time}'"
        )
        records.append(
            {"name": item.name, "price": item.price, "mod_time": item.mod_time.isoformat()}
        )

    return {"statusCode": 200, "body": json.dumps(records)}


def main(driver_name: str) -> dict:
    """Run main."""
    result = {"statusCode": 500, "body": "Internal Server Error."}
    try:
        with create_session(driver_name) as (session, metadata):
            t_0: float = time.time()
            logger.info(execute_query(session, metadata))
            t_1: float = time.time()
            logger.info(f"dt = {(t_1 - t_0):.3f}s")

    except sqlalchemy.exc.ProgrammingError as exc:
        logger.error(traceback.format_exc())
        logger.error(exc)
        result = {"statusCode": 500, "body": json.dumps(traceback.format_exc())}

    return result


if __name__ == "__main__":
    if sys.argv[1] in ["postgresql+pg8000", "postgresql+psycopg2"]:
        main(sys.argv[1])
    else:
        print(f"usage: {sys.argv[0]} " "{postgresql+pg8000|postgresql+psycopg2}", file=sys.stderr)

# EOF
