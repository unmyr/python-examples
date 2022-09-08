"""Example of sqlite3 with SQLAlchemy."""
from logging import getLogger, StreamHandler, DEBUG, Formatter
import datetime
import traceback
import typing

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
    Formatter('[%(asctime)s] %(levelname)s: %(message)s'))

Base = declarative_base()
engine: typing.Optional[sqlalchemy.engine.base.Engine] = None


class FruitsMenu(Base):
    """Fruits Menu."""
    __tablename__ = 'fruits_menu'

    id = Column(Integer, primary_key=True)  # emits SERIAL
    name = Column(String(16), unique=True)
    price = Column(Integer)
    # Default value is the creation time, not automatically updated
    mod_time = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    __table_args__ = (sqlalchemy.PrimaryKeyConstraint('id'), {
        'schema': 'guest'
    })

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self) -> str:
        mod_time_value = None
        if isinstance(self.mod_time, datetime.datetime):
            mod_time_value = self.mod_time.isoformat()

        return '{' + "id: {}, name: '{}', price: {}, mod_time: '{}'".format(
            self.id, self.name, self.price, mod_time_value) + '}'

    def to_dict(self) -> typing.Dict:
        """Generate non-primitive dict."""
        mod_time_value = None
        if isinstance(self.mod_time, datetime.datetime):
            mod_time_value = self.mod_time.isoformat()

        return {
            'name': self.name,
            'price': self.price,
            'mod_time': mod_time_value
        }


def handler() -> typing.Dict:
    """Run main."""
    result = {}

    try:
        global engine  # pylint: disable=global-statement
        if engine is None:
            logger.info('Call create_engine().')
            engine = sqlalchemy.create_engine(
                sqlalchemy.engine.URL.create(
                    drivername='sqlite',
                    host='',
                    port=None,
                    database=':memory:',
                    username='',
                    password=''
                ),
                echo=False
            )

            engine.execute(
                sqlalchemy.text("ATTACH DATABASE ':memory:' AS :schema"),
                schema='guest'
            )
            Base.metadata.create_all(bind=engine, checkfirst=True)

        inspector = sqlalchemy.inspect(engine)
        print(f"table_name={inspector.get_table_names()}")

        Session = sqlalchemy.orm.sessionmaker(engine)
        with engine.connect() as connection:
            with Session(bind=connection) as session:
                count = session.query(FruitsMenu).count()
                if count == 0:
                    session.add(FruitsMenu('Apple', 10))
                    session.add(FruitsMenu('Banana', 120))
                    session.add(FruitsMenu('Orange', 110))
                    session.commit()

                items = session.query(FruitsMenu).filter(
                    sqlalchemy.or_(
                        FruitsMenu.name == 'Apple',
                        FruitsMenu.name == 'Orange'
                    )
                ).all()

                records = []
                for item in items:
                    logger.info(item.to_dict())
                    records.append(item.to_dict())

                result['items'] = records

    except sqlalchemy.exc.ProgrammingError as exc:
        print(traceback.format_exc())
        print(exc)

    return result


def shutdown():
    """Dispose engine."""
    global engine  # pylint: disable=global-statement
    if engine is not None:
        logger.info('Call engine.dispose().')
        engine.dispose()
        engine = None


if __name__ == '__main__':
    print(handler())
    print(handler())
    shutdown()

# EOF
