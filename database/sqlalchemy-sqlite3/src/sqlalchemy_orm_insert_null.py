"""Example of sqlite3 with SQLAlchemy."""
import datetime
import traceback

from sqlalchemy.ext.declarative import declarative_base
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


def main(engine) -> None:
    """Run main."""
    try:
        engine.execute(
            sqlalchemy.text("ATTACH DATABASE ':memory:' AS :schema"),
            schema='guest'
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
    engine_sqlite3 = sqlalchemy.create_engine(
        db_uri,
        echo=False
    )
    main(engine_sqlite3)

# EOF
