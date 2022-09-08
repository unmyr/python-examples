# -*- coding: utf-8 -*-
"""Example of execute SELECT."""
from contextlib import contextmanager
import datetime
import json
import logging
import os
import sys
import time
import traceback
import typing

import sqlalchemy
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base

logger: logging.Logger = logging.getLogger(__name__)
stream_handler: logging.StreamHandler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.propagate = False
stream_handler.setFormatter(
    logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
)

Base = declarative_base()


class FruitsMenu(Base):
    """Fruits Menu."""
    __tablename__ = 'fruits_menu'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True
    )  # emits SERIAL
    name = sqlalchemy.Column(sqlalchemy.String(16), unique=True)
    price = sqlalchemy.Column(sqlalchemy.Integer)
    # Default value is the creation time, not automatically updated
    mod_time = sqlalchemy.Column(
        sqlalchemy.DateTime,
        server_default=sqlalchemy.sql.func.now()
    )
    __table_args__ = (
        sqlalchemy.PrimaryKeyConstraint('id'),
        {'schema': 'guest'}
    )


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
        db_name = 'fruits_menu.sqlite3'
        if os.path.exists(db_name):
            os.remove(db_name)
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
        engine.execute(
            sqlalchemy.text("ATTACH DATABASE ':memory:' AS :schema"),
            schema='guest'
        )

    Base.metadata.create_all(bind=engine, checkfirst=True)

    yield engine

    Base.metadata.drop_all(engine)
    engine.dispose()

    if driver_name == 'sqlite' and os.path.exists(db_name):
        os.remove(db_name)


def execute_query(
    driver_name: str,
    engine: sqlalchemy.engine.base.Engine
) -> typing.Dict:
    """Execute query."""
    query_results = []
    logger.info('engine.connect()')
    with engine.connect() as connection:
        trans = connection.begin()
        connection.execute(text("DELETE FROM guest.fruits_menu"))
        connection.execute(
            text(
                "INSERT INTO guest.fruits_menu (name, price) VALUES (:name, :price)"
            ),
            [
                {'name': 'Apple', 'price': 100},
                {'name': 'Banana', 'price': 120},
                {'name': 'Orange', 'price': -1},
                {'name': 'リンゴ', 'price': 180}
            ]
        )

        connection.execute(
            text("UPDATE guest.fruits_menu SET price=:price WHERE name = :name"),
            {'name': 'Orange', 'price': 110}
        )
        trans.commit()

        rows = connection.execute(text("SELECT * FROM guest.fruits_menu"))
        for row in rows:
            if driver_name.startswith('postgresql+'):
                # postgresql
                assert isinstance(row['mod_time'], datetime.datetime)
                mod_time_str = row['mod_time'].isoformat(timespec='seconds')
            else:
                # sqlite
                assert isinstance(row['mod_time'], str)
                mod_time_str = datetime.datetime.strptime(
                    row['mod_time'], '%Y-%m-%d %H:%M:%S'
                ).isoformat(timespec='seconds')
            print(f"row={row}")
            query_results.append({
                'id': row['id'],
                'name': row['name'],
                'price': row['price'],
                'mod_time': mod_time_str
            })

    return {'statusCode': 200, 'body': json.dumps(query_results)}


def main(driver_name: str) -> typing.Dict:
    """Run main."""
    result = {'statusCode': 500, 'body': 'Internal Server Error.'}
    try:
        with create_engine(driver_name) as engine:
            t_0 = time.time()
            logger.info(execute_query(driver_name, engine))
            t_1 = time.time()
            logger.info(f'dt = {(t_1 - t_0):.3f}s')

    except (sqlalchemy.exc.ProgrammingError, sqlalchemy.exc.InterfaceError,
            sqlalchemy.exc.OperationalError) as exc:
        # pg8000.exceptions.InterfaceError
        #  - Can't create a connection to host
        # psycopg2.OperationalError
        #  - could not connect to server: Connection refused
        logger.error(traceback.format_exc())
        logger.error(exc)
        result = {
            'statusCode': 500,
            'body': json.dumps(traceback.format_exc())
        }

    return result


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
