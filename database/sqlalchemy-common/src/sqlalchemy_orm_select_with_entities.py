"""Example of with_entities."""
import json
import logging
import os
import sys
import time
import traceback
import typing

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
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
    mod_time = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    __table_args__ = (
        sqlalchemy.PrimaryKeyConstraint('id'),
        {'schema': 'guest'}
    )

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return '{' + "id: {}, name: '{}', price: {}".format(
            self.id, self.name, self.price
        ) + '}'

    def to_dict(self) -> typing.Dict:
        """Generate non-primitive dict."""
        return {
            'name': self.name,
            'price': self.price
        }


class PerfInfo(typing.NamedTuple):
    """Performance information."""
    delta: float
    label: str


def execute_query(
    session: sqlalchemy.orm.session.Session
) -> typing.Tuple[typing.Dict, typing.Optional[typing.Iterable[PerfInfo]]]:
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
    query_obj = sqlalchemy.sql.expression.select(
        FruitsMenu.name,
        FruitsMenu.price
    ).filter(
        sqlalchemy.or_(
            FruitsMenu.name == 'Apple',
            FruitsMenu.name == 'Orange'
        )
    ).with_only_columns(FruitsMenu.name, FruitsMenu.price)
    items = session.execute(query_obj).mappings()

    t_3 = time.time()
    records = []
    row: typing.Mapping[typing.Any, typing.Any]
    print(f"items={items}, type={type(items).__module__}.{type(items).__name__}")
    for row in items:
        print(f"row={row}, type={type(row).__module__}.{type(row).__name__}")
        records.append([row['name'], row['price']])

    print("{}".format(query_obj.compile(compile_kwargs={'literal_binds': True})))

    result = {
        'statusCode': 200,
        'body': json.dumps(records)
    }
    t_4 = time.time()

    perf_list = (
        PerfInfo(round(t_4 - t_0, 3), 'Total'),
        PerfInfo(round(t_1 - t_0, 3), 'SELECT COUNT(id);'),
        PerfInfo(round(t_2 - t_1, 3), 'Insert records if the table is empty.'),
        PerfInfo(round(t_3 - t_2, 3), "SELECT id, name, price FROM fruit_menu WHERE name='Apple' OR name = 'Orange'"),
        PerfInfo(round(t_4 - t_3, 3), 'set response.'),
    )
    return result, perf_list


def main(driver_name: str) -> typing.Dict:
    """Run main."""
    result = {
        'statusCode': 500,
        'body': 'Internal Server Error.'
    }
    try:
        t_0 = time.time()
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
            with engine.connect() as conn:
                conn.execute(
                    sqlalchemy.text("ATTACH DATABASE ':memory:' AS :schema"),
                    {'schema': 'guest'}
                )

        t_1 = time.time()
        Base.metadata.create_all(bind=engine, checkfirst=True)

        t_2 = time.time()
        Session = sqlalchemy.orm.sessionmaker(engine)

        t_3 = time.time()
        perf_list_query: typing.Optional[typing.Iterable[PerfInfo]]
        with engine.connect() as connection:
            session: sqlalchemy.orm.session.Session
            with Session(bind=connection) as session:
                t_4 = time.time()
                result, perf_list_query = execute_query(session)
                t_5 = time.time()
                logger.info(result)

        t_6 = time.time()
        Base.metadata.drop_all(engine)
        t_7 = time.time()
        engine.dispose()
        if driver_name == 'sqlite' and os.path.exists(db_name):
            os.remove(db_name)
        t_8 = time.time()

        perf_list_main = (
            PerfInfo(round(t_8 - t_0, 3), 'Total'),
            PerfInfo(round(t_1 - t_0, 3), 'create_engine()'),
            PerfInfo(round(t_2 - t_1, 3), 'Base.metadata.create_all()'),
            PerfInfo(round(t_3 - t_2, 3), 'sessionmaker(engine)'),
            PerfInfo(round(t_4 - t_3, 3), 'engine.connect()'),
            PerfInfo(round(t_5 - t_4, 3), 'execute_query(session)'),
            PerfInfo(round(t_6 - t_5, 3), 'logger.info(result)'),
            PerfInfo(round(t_7 - t_6, 3), 'Base.metadata.drop_all(engine)'),
            PerfInfo(round(t_8 - t_7, 3), 'engine.dispose()')
        )
        item: PerfInfo
        print("\n*** subtotal of main ***")
        for item in perf_list_main:
            print(f"{item.delta:.3f}s {item.label}")

        if perf_list_query:
            print("\n*** subtotal of execute_query ***")
            for item in perf_list_query:
                print(f"{item.delta:.3f}s {item.label}")

    except sqlalchemy.exc.ProgrammingError as exc:
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
