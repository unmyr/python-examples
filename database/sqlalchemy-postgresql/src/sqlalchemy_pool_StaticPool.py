# -*- coding: utf-8 -*-
"""Example of StaticPool."""
import datetime
import logging
import os
import sys
import time
import typing
from contextlib import contextmanager

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

logger: logging.Logger = logging.getLogger(__name__)
stream_handler: logging.StreamHandler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.propagate = False
stream_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))

Base = declarative_base()


class FruitsMenu(Base):
    """Fruits Menu."""

    __tablename__ = "fruits_menu"

    id = Column(Integer, primary_key=True)  # emits SERIAL
    name = Column(String(16), unique=True)
    price = Column(Integer)
    # Default value is the creation time, not automatically updated
    mod_time = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    __table_args__ = (sqlalchemy.PrimaryKeyConstraint("id"), {"schema": "guest"})

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return (
            "{"
            + "id: {}, name: '{}', price: {}, mod_time: '{}'".format(
                self.id, self.name, self.price, self.mod_time.isoformat()
            )
            + "}"
        )

    def to_dict(self):
        """Generate non-primitive dict."""
        return {"name": self.name, "price": self.price, "mod_time": self.mod_time.isoformat()}


def optional_int(num_str: typing.Optional[str]) -> typing.Optional[int]:
    """Optional[str] to Optional[int]."""
    if num_str is None:
        return None
    return int(num_str)


@contextmanager
def create_engine(driver_name: str) -> typing.Generator[sqlalchemy.engine.base.Engine, None, None]:
    """Create engine."""
    engine = sqlalchemy.create_engine(
        sqlalchemy.engine.URL.create(
            driver_name,
            host=os.environ.get("PGHOST"),
            port=optional_int(os.environ.get("PGPORT")),
            database=os.environ.get("PGDATABASE"),
            username=os.environ.get("PGUSER"),
            password=os.environ.get("PGPASSWORD"),
        ),
        poolclass=sqlalchemy.pool.StaticPool,
    )
    yield engine
    time.sleep(10)
    print(f"{datetime.datetime.now()}: engine.dispose(): BEGIN")
    engine.dispose()
    print(f"{datetime.datetime.now()}: engine.dispose(): END")
    time.sleep(10)
    print(f"{datetime.datetime.now()}: process.exit()")


def main(driver_name: str):
    """Run main."""
    with create_engine(driver_name) as engine:
        t_0 = time.time()
        print(f"{datetime.datetime.now()}: sqlalchemy.orm.sessionmaker()()")
        session = sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)()
        print(f"{datetime.datetime.now()}: session.query(): BEGIN")
        count = session.query(FruitsMenu).count()
        t_1 = time.time()
        print(f"{datetime.datetime.now()}: session.query(): END")
        time.sleep(10)
        print(f"dt = {(t_1 - t_0):.3f}s; count={count}")


if __name__ == "__main__":
    if sys.argv[1] in ["postgresql+pg8000", "postgresql+psycopg2"]:
        main(sys.argv[1])
    else:
        print(f"usage: {sys.argv[0]} " "{postgresql+pg8000|postgresql+psycopg2}", file=sys.stderr)

# EOF
