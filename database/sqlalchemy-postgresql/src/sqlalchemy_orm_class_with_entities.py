"""Example of with_entities."""
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
    Column(DateTime, server_default=sqlalchemy.sql.func.now())
    __table_args__ = (
        sqlalchemy.PrimaryKeyConstraint('id'),
        {'schema': 'guest'}
    )

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return '{' + "id: {}, name: '{}', price: {}, modtime: '{}'".format(
            self.id, self.name, self.price, self.modtime.isoformat()
        ) + '}'

    def to_dict(self) -> typing.Dict:
        """Generate non-primitive dict."""
        return {
            'name': self.name,
            'price': self.price,
            'modtime': self.modtime.isoformat()
        }


def execute_query(
    session: sqlalchemy.orm.session.Session
) -> typing.Tuple[typing.Dict, typing.Optional[typing.List]]:
    """Execute query."""
    t_0 = time.time()
    count = session.query(
        sqlalchemy.func.count(FruitsMenu.id)
    ).scalar()
    t_1 = time.time()

    if count == 0:
        session.add(FruitsMenu('Apple', 10))
        session.add(FruitsMenu('Banana', 120))
        session.add(FruitsMenu('Orange', 110))
        session.commit()

    t_2 = time.time()
    query_obj = session.query(
        FruitsMenu
    ).filter(
        sqlalchemy.or_(
            FruitsMenu.name == 'Apple',
            FruitsMenu.name == 'Orange'
        )
    ).with_entities(
        FruitsMenu.name,
        FruitsMenu.price
    )
    items = query_obj.all()

    t_3 = time.time()
    records = []
    row: sqlalchemy.engine.row.Row
    for row in items:
        records.append([row['name'], row['price']])

    # stmt = query_obj.statement.compile(
    #     compile_kwargs={"literal_binds": True}
    # )
    # print("stmt:" + str(stmt))
    result = {
        'statusCode': 200,
        'body': json.dumps(records)
    }
    t_4 = time.time()

    perf_list = [
        round(t_4 - t_0, 3),
        round(t_1 - t_0, 3),
        round(t_2 - t_1, 3),
        round(t_3 - t_2, 3),
        round(t_4 - t_3, 3)
    ]
    return result, perf_list


def main(driver_name: str) -> typing.Dict:
    """Run main."""
    result = {
        'statusCode': 500,
        'body': 'Internal Server Error.'
    }
    try:
        t_0 = time.time()
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
            max_overflow=1,
            echo=False
        )

        t_1 = time.time()
        Base.metadata.create_all(bind=engine, checkfirst=True)

        t_2 = time.time()
        Session = sqlalchemy.orm.sessionmaker(engine)

        t_3 = time.time()
        perf_list_query: typing.Optional[typing.List]
        with engine.connect() as connection:
            session: sqlalchemy.orm.session.Session
            with Session(bind=connection) as session:
                t_4 = time.time()
                result, perf_list_query = execute_query(session)
                t_5 = time.time()
                logger.info(result)

        t_6 = time.time()
        engine.dispose()
        t_7 = time.time()

        perf_list_main = [
            round(t_7 - t_0, 3),
            round(t_1 - t_0, 3),
            round(t_2 - t_1, 3),
            round(t_3 - t_2, 3),
            round(t_4 - t_3, 3),
            round(t_5 - t_4, 3),
            round(t_6 - t_5, 3),
            round(t_7 - t_6, 3)
        ]
        logger.info(f'main={perf_list_main}, execute_query={perf_list_query}')

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
