"""Example of sqlalchemy.null."""
import datetime
import os
import sys
import traceback
import typing

from sqlalchemy.orm import declarative_base
import sqlalchemy


Base = declarative_base()


class DateTable(Base):
    """Example of nullable."""
    __tablename__ = 'date_table'

    data_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    entry_date = sqlalchemy.Column(sqlalchemy.Date, nullable=True)
    __table_args__ = ({
        'schema': 'guest'
    })

    def __init__(self, data_id, entry_date):
        self.data_id = data_id
        self.entry_date = entry_date


def main(driver_name: str) -> None:
    """Run main."""
    config: typing.Dict[str, typing.Any] = {}
    if driver_name == 'sqlite':
        db_name = 'date_table.sqlite3'
        db_uri = sqlalchemy.engine.URL.create(
            drivername=driver_name,
            host='',
            port=None,
            database=':memory:',
            username='',
            password=''
        )
        if os.path.exists(db_name):
            os.remove(db_name)
    else:
        db_uri = sqlalchemy.engine.URL.create(
            driver_name,
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

    try:
        engine: sqlalchemy.engine.base.Engine = sqlalchemy.create_engine(
            db_uri,
            **config,
            echo=False
        )

        if driver_name == 'sqlite':
            with engine.begin() as conn:
                conn.execute(
                    sqlalchemy.text("ATTACH DATABASE ':memory:' AS :schema"),
                    {'schema': 'guest'}
                )

        Base.metadata.create_all(bind=engine, checkfirst=True)

        Session = sqlalchemy.orm.sessionmaker(engine)
        with engine.connect() as connection:
            with Session(bind=connection) as session:
                item: DateTable
                count = session.query(DateTable).count()
                if count == 0:
                    session.add(
                        DateTable(1, datetime.date.today())
                    )
                    session.add(
                        DateTable(2, sqlalchemy.null())
                    )
                    session.add(
                        DateTable(3, datetime.date(2021, 1, 1))
                    )
                    session.add(
                        DateTable(4, sqlalchemy.null())
                    )
                    session.commit()

                items = session.query(DateTable).filter(
                    DateTable.entry_date == sqlalchemy.null()
                ).all()
                for item in items:
                    print({
                        'data_id': item.data_id,
                        'entry_date': item.entry_date
                    })

        Base.metadata.drop_all(engine)

    except sqlalchemy.exc.ProgrammingError as exc:
        print(traceback.format_exc())
        print(exc)

    finally:
        if driver_name == 'sqlite' and os.path.exists(db_name):
            os.remove(db_name)


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
