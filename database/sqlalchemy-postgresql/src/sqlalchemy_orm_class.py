# -*- coding: utf-8 -*-
"""Example of execute SELECT."""
from contextlib import contextmanager
from logging import getLogger, StreamHandler, DEBUG, Formatter
import json
import os
import sys
import time
import traceback

from sqlalchemy import Column, Integer, String, DateTime
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


class FruitsMenu(Base):
    """Fruits Menu."""
    __tablename__ = 'fruitsmenu'

    schema = 'public'
    id = Column(Integer, primary_key=True)
    name = Column(String(16), unique=True)
    price = Column(Integer)
    modtime = Column(DateTime)

    def __init__(self, name, price, modtime):
        self.name = name
        self.price = price
        self.modtime = modtime

    def __str__(self):
        return 'id:{}, name:{}, price:{}, modtime:{}'.format(self.id, self.name, self.price, self.modtime)

    def to_dict(self):
        """Generate non-primitive dict."""
        return {
            'name': self.name,
            'price': self.price,
            'modtime': self.modtime.isoformat()
        }


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

    Session = sqlalchemy.orm.sessionmaker(engine)
    with engine.connect() as connection:
        with Session(bind=connection) as session:
            yield session
    engine.dispose()


def execute_query(session):
    """Execute query."""
    logger.info('engine.connect()')

    items = session.query(
        FruitsMenu
    ).filter(
        FruitsMenu.name == 'Apple'
    ).all()
    logger.info(items)

    records = []
    for item in items:
        logger.info(item)
        records.append(item.to_dict())

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
        with create_session(driver_name) as session:
            t_0 = time.time()
            logger.info(execute_query(session))
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
