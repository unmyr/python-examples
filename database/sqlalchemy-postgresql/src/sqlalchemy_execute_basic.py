# -*- coding: utf-8 -*-
"""Example of execute SELECT."""
from contextlib import contextmanager
import json
import logging
import os
import sys
import time
import traceback
import typing

import sqlalchemy
from sqlalchemy import text

logger: logging.Logger = logging.getLogger(__name__)
stream_handler: logging.StreamHandler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.propagate = False
stream_handler.setFormatter(
    logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
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
    engine = sqlalchemy.create_engine(
        sqlalchemy.engine.URL.create(
            driver_name,
            host=os.environ.get('PGHOST'),
            port=optional_int(os.environ.get('PGPORT')),
            database=os.environ.get('PGDATABASE'),
            username=os.environ.get('PGUSER'),
            password=os.environ.get('PGPASSWORD')
        ),
        pool_size=1,
        max_overflow=1
    )
    yield engine
    engine.dispose()


def execute_query(engine) -> typing.Dict:
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
            query_results.append({
                'id': row['id'],
                'name': row['name'],
                'price': row['price'],
                'modtime': row['modtime'].isoformat()  # datetime.datetime
            })

    return {'statusCode': 200, 'body': json.dumps(query_results)}


def main(driver_name):
    """Run main."""
    result = {'statusCode': 500, 'body': 'Internal Server Error.'}
    try:
        with create_engine(driver_name) as engine:
            t_0 = time.time()
            logger.info(execute_query(engine))
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
    if sys.argv[1] in ['postgresql+pg8000', 'postgresql+psycopg2']:
        main(sys.argv[1])
    else:
        print(
            f"usage: {sys.argv[0]} "
            '{postgresql+pg8000|postgresql+psycopg2}',
            file=sys.stderr
        )

# EOF
