"""Example of ORM."""
import json
import logging
import os
import random
import sys
import time
import traceback
import typing
from contextlib import contextmanager

import sqlalchemy
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

    def __str__(self) -> str:
        if self.mod_time:
            return (
                "{"
                + "id: {}, name: '{}', price: {}, mod_time: '{}'".format(
                    self.id, self.name, self.price, self.mod_time.isoformat()
                )
                + "}"
            )
        else:
            return (
                "{"
                + "id: {}, name: '{}', price: {}, mod_time: {}".format(
                    self.id, self.name, self.price, self.mod_time
                )
                + "}"
            )

    def to_dict(self) -> typing.Dict:
        """Generate non-primitive dict."""
        if self.mod_time:
            result_dict = {
                "name": self.name,
                "price": self.price,
                "mod_time": self.mod_time.isoformat(),
            }
        else:
            result_dict = {"name": self.name, "price": self.price, "mod_time": None}
        return result_dict


@contextmanager
def create_session(
    driver_name: str,
) -> typing.Generator[sqlalchemy.orm.session.Session, None, None]:
    """Create engine."""
    config: typing.Dict
    if driver_name == "sqlite":
        db_name = "fruits_menu.sqlite3"
        if os.path.exists(db_name):
            os.remove(db_name)
        db_uri = sqlalchemy.engine.URL.create(
            drivername=driver_name,
            host="",
            port=None,
            database=":memory:",
            username="",
            password="",
        )
        config = dict()
    else:
        db_uri = sqlalchemy.engine.URL.create(
            drivername=driver_name,
            host=os.environ.get("PGHOST"),
            port=typing.cast(int, os.environ.get("PGPORT")),
            database=os.environ.get("PGDATABASE"),
            username=os.environ.get("PGUSER"),
            password=os.environ.get("PGPASSWORD"),
        )
        config = dict(pool_size=1, max_overflow=1)

    engine = sqlalchemy.create_engine(db_uri, **config, echo=False)
    if driver_name == "sqlite":
        with engine.connect() as conn:
            conn.execute(
                sqlalchemy.text("ATTACH DATABASE ':memory:' AS :schema"), {"schema": "guest"}
            )

    Base.metadata.create_all(bind=engine, checkfirst=True)

    Session = sqlalchemy.orm.sessionmaker(engine)
    with engine.connect() as connection:
        session: sqlalchemy.orm.session.Session
        with Session(bind=connection) as session:
            yield session

    Base.metadata.drop_all(engine)

    engine.dispose()

    if driver_name == "sqlite" and os.path.exists(db_name):
        os.remove(db_name)


def execute_query(session: sqlalchemy.orm.session.Session) -> typing.Dict:
    """Execute query."""
    logger.info("engine.connect()")

    count = session.query(FruitsMenu).count()
    if count == 0:
        session.add(FruitsMenu("Apple", 10))
        session.add(FruitsMenu("Banana", 120))
        session.add(FruitsMenu("Orange", 110))
        session.commit()

    items = (
        session.query(FruitsMenu)
        .filter(sqlalchemy.or_(FruitsMenu.name == "Apple", FruitsMenu.name == "Orange"))
        .all()
    )

    update_count = (
        session.query(FruitsMenu)
        .filter(sqlalchemy.or_(FruitsMenu.name == "Apple"))
        .update({FruitsMenu.price: random.randrange(100, 200)})
    )
    session.commit()
    print(update_count)

    items = session.query(FruitsMenu).all()

    records = []
    for item in items:
        logger.info(item)
        records.append(item.to_dict())

    return {"statusCode": 200, "body": json.dumps(records)}


def main(driver_name: str) -> typing.Dict:
    """Run main."""
    result = {"statusCode": 500, "body": "Internal Server Error."}
    try:
        session: sqlalchemy.orm.session.Session
        with create_session(driver_name) as session:
            t_0 = time.time()
            logger.info(execute_query(session))
            t_1 = time.time()
            logger.info(f"dt = {(t_1 - t_0):.3f}s")

    except sqlalchemy.exc.ProgrammingError as exc:
        logger.error(traceback.format_exc())
        logger.error(exc)
        result = {"statusCode": 500, "body": json.dumps(traceback.format_exc())}

    return result


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main("sqlite")
    elif len(sys.argv) == 2 and sys.argv[1] in [
        "sqlite",
        "postgresql+pg8000",
        "postgresql+psycopg2",
    ]:
        main(sys.argv[1])
    else:
        print(
            f"usage: {sys.argv[0]} " "{sqlite|postgresql+pg8000|postgresql+psycopg2}",
            file=sys.stderr,
        )

# EOF
