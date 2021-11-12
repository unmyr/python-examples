"""Example of sqlite3 with SQLAlchemy."""
import os
import time
import traceback

from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy


Base = declarative_base()


class Customers(Base):
    """Names of people."""
    __tablename__ = 'customers'
    cid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(255))
    __table_args__ = ({'schema': 'guest'})

    def __init__(self, name):
        self.name = name


def insert_sqlalchemy_orm_core(
    engine: sqlalchemy.engine.base.Engine,
    count: int
) -> float:
    """SQLAlcemy Core."""
    Base.metadata.create_all(bind=engine, checkfirst=True)

    t_0 = time.time()
    engine.execute(
        Customers.__table__.insert(),
        [dict(name=f'NAME {i:010d}') for i in range(count)]
    )
    t_1 = time.time()
    dt = t_1 - t_0

    Base.metadata.drop_all(engine)

    return dt


def insert_sqlalchemy_orm_bulk_insert_mappings(
    engine: sqlalchemy.engine.base.Engine,
    count: int
) -> float:
    """Insert with Session#bulk_insert_mappings()."""
    Base.metadata.create_all(bind=engine, checkfirst=True)

    with engine.connect() as connection:
        Session = sqlalchemy.orm.sessionmaker(engine)
        with Session(bind=connection) as session:
            t_0 = time.time()
            session.bulk_insert_mappings(
                Customers,
                [{'name': f'NAME {i:010d}'} for i in range(count)]
            )
            session.commit()
            t_1 = time.time()
            dt = t_1 - t_0

    Base.metadata.drop_all(engine)

    return dt


def insert_sqlalchemy_orm_bulk_save_objects(
    engine: sqlalchemy.engine.base.Engine,
    count: int
) -> float:
    """Insert with Session#bulk_save_objects()."""
    Base.metadata.create_all(bind=engine, checkfirst=True)

    with engine.connect() as connection:
        Session = sqlalchemy.orm.sessionmaker(engine)
        with Session(bind=connection) as session:
            t_0 = time.time()
            session.bulk_save_objects(
                [Customers(f'NAME {i:010d}') for i in range(count)]
            )
            session.commit()
            t_1 = time.time()
            dt = t_1 - t_0

    Base.metadata.drop_all(engine)

    return dt


def insert_sqlalchemy_orm_add(
    engine: sqlalchemy.engine.base.Engine,
    count: int
) -> float:
    """Insert with Session#add()."""
    Base.metadata.create_all(engine)

    with engine.connect() as connection:
        Session = sqlalchemy.orm.sessionmaker(engine)
        with Session(bind=connection) as session:
            t_0 = time.time()
            for i in range(count):
                session.add(Customers(f'NAME {i:010d}'))
                if i % 1000 == 999:
                    session.flush()
            session.commit()
            t_1 = time.time()
            dt = t_1 - t_0

    return dt


def main() -> None:
    """Run main."""
    db_name = 'customers.sqlite3'
    db_uri = sqlalchemy.engine.URL.create(
        drivername='sqlite',
        host='',
        port=None,
        database=':memory:',
        username='',
        password=''
    )

    if os.path.exists(db_name):
        os.remove(db_name)

    count = 10000
    try:
        engine = sqlalchemy.create_engine(
            db_uri,
            echo=False
        )

        engine.execute(
            sqlalchemy.text(f"ATTACH DATABASE '{db_name}' AS :schema"),
            schema='guest'
        )

        print("[ SQLAlchemy Core ]")
        dt = insert_sqlalchemy_orm_core(engine, count)
        print(f"{'%6.2f' % dt} [s/{count}records]   {1000 * dt / count:.3f} [ms/records]")

        print("[ BULK INSERT (bulk_insert_mappings) ]")
        dt = insert_sqlalchemy_orm_bulk_insert_mappings(engine, count)
        print(f"{'%6.2f' % dt} [s/{count}records]   {1000 * dt / count:.3f} [ms/records]")

        print("[ BULK INSERT (bulk_save_objects) ]")
        dt = insert_sqlalchemy_orm_bulk_save_objects(engine, count)
        print(f"{'%6.2f' % dt} [s/{count}records]   {1000 * dt / count:.3f} [ms/records]")

        print("[ NORMAL INSERT ]")
        dt = insert_sqlalchemy_orm_add(engine, count)
        print(f"{'%6.2f' % dt} [s/{count}records]   {1000 * dt / count:.3f} [ms/records]")

    except sqlalchemy.exc.ProgrammingError as exc:
        print(traceback.format_exc())
        print(exc)

    finally:
        if os.path.exists(db_name):
            os.remove(db_name)


if __name__ == '__main__':
    main()

# EOF
