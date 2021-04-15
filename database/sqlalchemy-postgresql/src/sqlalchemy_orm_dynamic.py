# -*- coding: utf-8 -*-
"""Example of execute SELECT."""
from contextlib import contextmanager
from logging import getLogger, StreamHandler, DEBUG, Formatter
import json
import os
import sys
import time
import traceback

from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy


logger = getLogger(__name__)
stream_handler = StreamHandler()
stream_handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(stream_handler)
logger.propagate = False
stream_handler.setFormatter(
    Formatter('[%(asctime)s] %(levelname)s: %(message)s')
)

Base = declarative_base()


class FruitsMenu(object):
    """OR Mapper for FRUITS_MENU table."""


@contextmanager
def create_session(driver_name: str):
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
    metadata = sqlalchemy.MetaData(engine)

    Session = sqlalchemy.orm.sessionmaker(engine)
    with engine.connect() as connection:
        logger.info('engine.connect()')
        with Session(bind=connection) as session:
            yield session, metadata
        logger.info('engine.close()')
    logger.info('engine.dispose()')
    engine.dispose()


def execute_query(session, metadata):
    """Execute query."""
    # meta.create_all()

    columns = (
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column('name', sqlalchemy.String(length=16), unique=True),
        sqlalchemy.Column('price', sqlalchemy.Integer),
        sqlalchemy.Column('modtime', sqlalchemy.DateTime),
    )
    fruit_item_table = sqlalchemy.Table(
        "fruits_menu",
        metadata,
        *columns,
        schema='guest'
    )
    sqlalchemy.orm.mapper(FruitsMenu, fruit_item_table)

    items = session.query(
        FruitsMenu
    ).filter(
        sqlalchemy.or_(
            FruitsMenu.name == 'Apple',  # pylint: disable=no-member
            FruitsMenu.name == 'Orange'  # pylint: disable=no-member
        )
    ).all()
    logger.info(f"Total: {len(items)} items.")

    records = []
    for item in items:
        logger.info(f"id={item.id} name='{item.name}' price={item.price} modtime='{item.modtime}'")
        records.append(
            {
                'name': item.name,
                'price': item.price,
                'modtime': item.modtime.isoformat()
            }
        )

    return {
        'statusCode': 200,
        'body': json.dumps(records)
    }


def main(driver_name):
    """Run main."""
    result = {
        'statusCode': 500,
        'body': 'Internal Server Error.'
    }
    try:
        with create_session(driver_name) as (session, metadata):
            t_0 = time.time()
            logger.info(execute_query(session, metadata))
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
