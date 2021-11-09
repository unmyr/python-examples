"""Example of sqlite3 with SQLAlchemy."""
from logging import getLogger, StreamHandler, DEBUG, Formatter
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
    Formatter('[%(asctime)s] %(levelname)s: %(message)s'))

Base = declarative_base()


class FruitsMenu(Base):
    """Fruits Menu."""
    __tablename__ = 'fruits_menu'

    id = Column(Integer, primary_key=True)  # emits SERIAL
    name = Column(String(16), unique=True)
    price = Column(Integer)
    # Default value is the creation time, not automatically updated
    modtime = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    __table_args__ = (sqlalchemy.PrimaryKeyConstraint('id'), {
        'schema': 'guest'
    })

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return '{' + "id: {}, name: '{}', price: {}, modtime: '{}'".format(
            self.id, self.name, self.price, self.modtime.isoformat()) + '}'

    def to_dict(self):
        """Generate non-primitive dict."""
        return {
            'name': self.name,
            'price': self.price,
            'modtime': self.modtime.isoformat()
        }


def main(engine):
    """Run main."""
    try:
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
                    sqlalchemy.or_(FruitsMenu.name == 'Apple',
                                   FruitsMenu.name == 'Orange')).all()
                # logger.info(items)
                records = []
                for item in items:
                    logger.info(item)
                    records.append(item.to_dict())

    except sqlalchemy.exc.ProgrammingError as exc:
        print(traceback.format_exc())
        print(exc)


if __name__ == '__main__':
    db_uri = sqlalchemy.engine.URL.create(
        drivername='sqlite',
        host='',
        port=None,
        database=':memory:',
        username='',
        password=''
    )
    print(db_uri)
    engine_sqlite3 = sqlalchemy.create_engine(
        db_uri,
        echo=False
    )
    main(engine_sqlite3)

# EOF
