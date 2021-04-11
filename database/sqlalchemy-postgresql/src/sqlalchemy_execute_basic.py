# -*- coding: utf-8 -*-
"""Example of execute SELECT."""
from contextlib import contextmanager
from logging import getLogger, StreamHandler, DEBUG, Formatter
import json
import os
import sys
import time
import traceback

import sqlalchemy
from sqlalchemy import text


logger = getLogger(__name__)
stream_handler = StreamHandler()
stream_handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(stream_handler)
logger.propagate = False
stream_handler.setFormatter(
    Formatter('[%(asctime)s] %(levelname)s: %(message)s')
)


@contextmanager
def create_engine(driver_name: str):
    """Create engine."""
    engine = sqlalchemy.create_engine(
        sqlalchemy.engine.URL.create(
            driver_name,
            host=os.environ.get('PGHOST'),
            port=os.environ.get('PGPORT'),
            database=os.environ.get('PGDATABASE'),
            username=os.environ.get('PGUSER'),
            password=os.environ.get('PGPASSWORD')
        ),
        pool_size=1,
        max_overflow=1
    )
    yield engine
    engine.dispose()


def execute_query(engine):
    """Execute query."""
    query_results = []
    logger.info('engine.connect()')
    with engine.connect() as connection:
        trans = connection.begin()
        connection.execute(
            text("DELETE FROM FruitsMenu")
        )
        connection.execute(
            text("INSERT INTO FruitsMenu (name, price) VALUES (:name, :price)"),
            [
                {'name': 'Apple', 'price': 100},
                {'name': 'Banana', 'price': 120},
                {'name': 'Orange', 'price': -1},
                {'name': 'リンゴ', 'price': 180}
            ]
        )

        connection.execute(
            text("UPDATE FruitsMenu SET price=:price WHERE name = :name"),
            {'name': 'Orange', 'price': 110}
        )
        trans.commit()

        rows = connection.execute(
            text("SELECT * FROM FruitsMenu")
        )
        for row in rows:
            query_results.append(
                {
                    'id': row['id'],
                    'name': row['name'],
                    'price': row['price'],
                    'modtime': row['modtime'].isoformat()  # datetime.datetime
                }
            )

    return {
        'statusCode': 200,
        'body': json.dumps(query_results)
    }


def main(driver_name):
    """Run main."""
    result = {
        'statusCode': 500,
        'body': 'Internal Server Error.'
    }
    try:
        with create_engine(driver_name) as engine:
            t_0 = time.time()
            logger.info(execute_query(engine))
            t_1 = time.time()
            logger.info(f'dt = {(t_1 - t_0):.3f}s')

    except sqlalchemy.exc.ProgrammingError as exc:
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
        print("usage: {sys.argv[0]} " + '{postgresql+pg8000|postgresql+psycopg2}', sys.stderr)

# EOF
