"""Example of ORM."""
from contextlib import contextmanager
import json
import logging
import os
import sys
import time
import traceback
import typing

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy


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

    id = Column(Integer, primary_key=True)  # emits SERIAL
    name = Column(String(16), unique=True)
    price = Column(Integer)
    # Default value is the creation time, not automatically updated
    modtime = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    __table_args__ = (
        sqlalchemy.PrimaryKeyConstraint('id'),
        {'schema': 'guest'}
    )

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self) -> str:
        if self.modtime:
            return '{' + "id: {}, name: '{}', price: {}, modtime: '{}'".format(
                self.id, self.name, self.price, self.modtime.isoformat()
            ) + '}'
        else:
            return '{' + "id: {}, name: '{}', price: {}, modtime: {}".format(
                self.id, self.name, self.price, self.modtime
            ) + '}'

    def to_dict(self) -> typing.Dict:
        """Generate non-primitive dict."""
        if self.modtime:
            result_dict = {
                'name': self.name,
                'price': self.price,
                'modtime': self.modtime.isoformat()
            }
        else:
            result_dict = {
                'name': self.name,
                'price': self.price,
                'modtime': None
            }
        return result_dict


@contextmanager
def create_session(driver_name):
    """Create engine."""
    engine: sqlalchemy.engine.base.Engine = sqlalchemy.create_engine(
        sqlalchemy.engine.URL.create(
            driver_name,
            host=os.environ.get('PGHOST'),
            port=typing.cast(int, os.environ.get('PGPORT')),
            database=os.environ.get('PGDATABASE'),
            username=os.environ.get('PGUSER'),
            password=os.environ.get('PGPASSWORD')
        ),
        pool_size=1,
        max_overflow=1
    )
    Base.metadata.create_all(bind=engine, checkfirst=True)

    Session = sqlalchemy.orm.sessionmaker(engine)
    with engine.connect() as connection:
        session: sqlalchemy.orm.session.Session
        with Session(bind=connection) as session:
            yield session
    engine.dispose()


def execute_query(
    session: sqlalchemy.orm.session.Session
) -> typing.Dict:
    """Execute query."""
    logger.info('engine.connect()')

    count = session.query(
        FruitsMenu
    ).count()
    if count == 0:
        session.add(FruitsMenu('Apple', 10))
        session.add(FruitsMenu('Banana', 120))
        session.add(FruitsMenu('Orange', 110))
        session.commit()

    items = session.query(
        FruitsMenu
    ).filter(
        sqlalchemy.or_(
            FruitsMenu.name == 'Apple',
            FruitsMenu.name == 'Orange'
        )
    ).all()
    # logger.info(items)

    records = []
    for item in items:
        logger.info(item)
        records.append(item.to_dict())

    return {
        'statusCode': 200,
        'body': json.dumps(records)
    }


def main(driver_name: str) -> typing.Dict:
    """Run main."""
    result = {
        'statusCode': 500,
        'body': 'Internal Server Error.'
    }
    try:
        session: sqlalchemy.orm.session.Session
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
        print(
            f"usage: {sys.argv[0]} "
            '{postgresql+pg8000|postgresql+psycopg2}',
            file=sys.stderr
        )

# EOF
