"""An example of schema usage."""
import logging
import os
import sys
import traceback
import typing

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
import sqlalchemy
import sqlalchemy.orm


class BraceMessage:
    """Brace message"""
    def __init__(self, fmt, *args, **kwargs) -> None:
        self.fmt = fmt
        self.args = args
        self.kwargs = kwargs

    def __str__(self) -> str:
        return self.fmt.format(*self.args, **self.kwargs)


__ = BraceMessage

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


def optional_int(
    num_str: typing.Optional[str]
) -> typing.Optional[int]:
    """Optional[str] to Optional[int]."""
    return None if num_str is None else int(num_str)


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
        {'schema': 'dummy_schema'}
    )

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return '{' + "id: {}, name: '{}', price: {}, mod_time: '{}'".format(
            self.id, self.name, self.price, self.mod_time.isoformat()
        ) + '}'

    def to_dict(self):
        """Generate non-primitive dict."""
        return {
            'name': self.name,
            'price': self.price,
            'mod_time': self.mod_time.isoformat()
        }


def select_all(session: sqlalchemy.orm.session.Session) -> typing.List[typing.Tuple]:
    """Run main."""
    try:
        query_obj = session.query(
            FruitsMenu
        ).filter(
            sqlalchemy.or_(
                FruitsMenu.name == 'Apple',
                FruitsMenu.name == 'Orange'
            )
        )
        items = query_obj.all()

        records = []
        item: FruitsMenu
        for item in items:
            records.append(item.to_dict())

        return records

    except sqlalchemy.exc.ProgrammingError as exc:
        print(traceback.format_exc())
        print(exc)

    return []


def main(driver_name: str) -> None:
    """Run main."""
    config: typing.Dict
    if driver_name == 'sqlite':
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

    # Get metadata (version, schema)
    logger.info(__('create_engine(...)'))
    default_schema = 'guest'
    engine: sqlalchemy.engine.base.Engine = sqlalchemy.create_engine(
        db_uri,
        **config,
        execution_options={"schema_translate_map": {"dummy_schema": default_schema}},
        echo=True
    )

    # Create schema
    logger.info(__('engine.connect()'))
    with engine.connect() as conn:
        logger.info(__('Create schema.'))
        if driver_name == 'sqlite':
            # SQLite has no attribute 'has_schema'
            conn.execute(
                sqlalchemy.text("ATTACH DATABASE ':memory:' AS :schema"),
                {"schema": default_schema}
            )
        elif engine.dialect.has_schema(conn, default_schema):
            pass
        else:
            conn.execute(
                sqlalchemy.schema.CreateSchema(default_schema)
            )

    # Create tables
    logger.info(__('Base.metadata.create_all(bind=engine, checkfirst=True)'))
    Base.metadata.create_all(bind=engine, checkfirst=True)

    Session = sqlalchemy.orm.sessionmaker(engine)
    with engine.connect() as connection:
        with Session(bind=connection) as session:
            if session.query(FruitsMenu).count() == 0:
                session.bulk_save_objects(
                    [
                        FruitsMenu('Apple', 10),
                        FruitsMenu('Banana', 120),
                        FruitsMenu('Orange', 110)
                    ]
                )
                session.commit()
            for row in select_all(session):
                print(row)

    # Drop tables
    logger.info(__('Base.metadata.drop_all(engine)'))
    Base.metadata.drop_all(engine)

    # Disconnect connections, etc.
    logger.info(__('engine.dispose()'))
    engine.dispose()


def usage(command_name: str):
    """Usage."""
    print(
        f"usage: {command_name} "
        '{sqlite|postgresql+pg8000|postgresql+psycopg2}',
        file=sys.stderr
    )


if __name__ == '__main__':
    drivers = ['sqlite', 'postgresql+pg8000', 'postgresql+psycopg2']
    if len(sys.argv) == 2 and sys.argv[1] in drivers:
        main(sys.argv[1])
    else:
        usage(sys.argv[0])

# EOF
