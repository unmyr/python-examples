"""Example of sqlite3 with SQLAlchemy."""
import os
import sys
import time
import traceback
import typing

from sqlalchemy.orm import declarative_base  # pylint: disable=unused-import
import sqlalchemy


Base = sqlalchemy.orm.declarative_base()


class Customers(Base):
    """Names of people."""
    __tablename__ = 'customers'
    cid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(255))
    status = sqlalchemy.Column(sqlalchemy.Integer)
    email = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)
    __table_args__ = ({'schema': 'guest'})

    def __init__(self, name, status=None, email=None):
        self.name = name
        self.status = status
        self.email = email


def insert_records(
    engine: sqlalchemy.engine.base.Engine,
    count: int
) -> float:
    """Insert records"""
    t_0 = time.time()
    with engine.begin() as connection:
        connection.execute(
            Customers.__table__.insert(),
            [dict(name=f'NAME {i:010d}', status=0, email=None) for i in range(count)]
        )
    t_1 = time.time()
    return t_1 - t_0


def update_same_value_sqlalchemy_orm_core(
    engine: sqlalchemy.engine.base.Engine,
    count: int
) -> typing.Tuple[float, float]:
    """SQLAlchemy Core."""
    Base.metadata.create_all(bind=engine, checkfirst=True)

    dt_ins = insert_records(engine, count)

    t_0 = time.time()
    with engine.begin() as connection:
        connection.execute(
            Customers.__table__.update().values(status=1234)
        )
    t_1 = time.time()

    Base.metadata.drop_all(engine)

    return dt_ins, t_1 - t_0


def sqlalchemy_orm_bulk_update_mappings(
    engine: sqlalchemy.engine.base.Engine,
    count: int
) -> typing.Tuple[float, float]:
    """Update with Session#bulk_update_mappings()."""
    Base.metadata.create_all(bind=engine, checkfirst=True)

    dt_ins = insert_records(engine, count)

    with engine.connect() as connection:
        Session = sqlalchemy.orm.sessionmaker(engine)
        with Session(bind=connection) as session:
            t_0 = time.time()
            mappings = []
            i = 0
            for item in session.query(Customers).all():
                map_value = {
                    'cid': item.cid,
                    'email': f'name-{i:010d}@example.com',
                    'status': 1234
                }
                mappings.append(map_value)
                if i % 10000 == 9999:
                    session.bulk_update_mappings(Customers, mappings)
                    session.commit()
                    mappings[:] = []
                i += 1

            if len(mappings) > 0:
                session.bulk_update_mappings(Customers, mappings)
                session.commit()
                mappings[:] = []
            t_1 = time.time()

    Base.metadata.drop_all(engine)

    return dt_ins, t_1 - t_0


def sqlalchemy_orm_bulk_save_objects_update(
    engine: sqlalchemy.engine.base.Engine,
    count: int
) -> typing.Tuple[float, float]:
    """Update with Session#bulk_save_objects()."""
    Base.metadata.create_all(bind=engine, checkfirst=True)

    dt_ins = insert_records(engine, count)

    with engine.connect() as connection:
        Session = sqlalchemy.orm.sessionmaker(engine)
        with Session(bind=connection) as session:
            t_0 = time.time()
            customers = []
            i = 0
            for item in session.query(Customers).all():
                item.status = 1234
                item.email = f'name-{i:010d}@example.com'
                customers.append(item)
                if i % 10000 == 9999:
                    session.bulk_save_objects(customers)
                    session.commit()
                    customers[:] = []
                i += 1

            if len(customers) > 0:
                session.bulk_save_objects(customers, update_changed_only=False)
                session.commit()
                customers[:] = []
            t_1 = time.time()

    Base.metadata.drop_all(engine)

    return dt_ins, t_1 - t_0


def sqlalchemy_orm_update_same_value(
    engine: sqlalchemy.engine.base.Engine,
    count: int
) -> typing.Tuple[float, float]:
    """Update with Statement#update()."""
    Base.metadata.create_all(engine)

    dt_ins = insert_records(engine, count)

    with engine.connect() as connection:
        Session = sqlalchemy.orm.sessionmaker(engine)
        with Session(bind=connection) as session:
            t_0 = time.time()
            session.query(Customers).update({
                Customers.status: 1234
            })
            session.commit()
            t_1 = time.time()

    Base.metadata.drop_all(engine)

    return dt_ins, t_1 - t_0


def sqlalchemy_orm_update_deferent_values(
    engine: sqlalchemy.engine.base.Engine,
    count: int
) -> typing.Tuple[float, float]:
    """Update with Statement#update()."""
    Base.metadata.create_all(engine)

    dt_ins = insert_records(engine, count)

    with engine.connect() as connection:
        Session = sqlalchemy.orm.sessionmaker(engine)
        with Session(bind=connection) as session:
            t_0 = time.time()
            i = 0
            for item in session.query(Customers).all():
                item.status = 1234
                item.email = f'name-{i:010d}@example.com'
                i += 1
            session.commit()
            t_1 = time.time()

    Base.metadata.drop_all(engine)

    return dt_ins, t_1 - t_0


def main(driver_name: str) -> None:
    """Run main."""
    config = {}
    if driver_name == 'sqlite':
        db_name = 'customers.sqlite3'
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

    try:
        engine = sqlalchemy.create_engine(
            db_uri,
            **config,
            echo=False
        )

        if driver_name == 'sqlite':
            with engine.begin() as connection:
                connection.execute(
                    sqlalchemy.text(f"ATTACH DATABASE '{db_name}' AS :schema"),
                    {'schema': 'guest'}
                )

        count = 10000
        print("--- Update same value ---")
        print("[ SQLAlchemy Core ]")
        _, dt_upd = update_same_value_sqlalchemy_orm_core(engine, count)
        print(f"{'%6.2f' % dt_upd} [s/{count}records]   {1000 * dt_upd / count:.3f} [ms/records]")

        print("[ ORM UPDATE same value ]")
        _, dt_upd = sqlalchemy_orm_update_same_value(engine, count)
        print(f"{'%6.2f' % dt_upd} [s/{count}records]   {1000 * dt_upd / count:.3f} [ms/records]")
        print()

        count = 1000
        print("--- Update deferent value ---")
        print("[ BULK UPDATE (bulk_update_mappings) ]")
        _, dt_upd = sqlalchemy_orm_bulk_update_mappings(engine, count)
        print(f"{'%6.2f' % dt_upd} [s/{count}records]   {1000 * dt_upd / count:.3f} [ms/records]")

        print("[ BULK UPDATE (bulk_save_objects) ]")
        _, dt_upd = sqlalchemy_orm_bulk_save_objects_update(engine, count)
        print(f"{'%6.2f' % dt_upd} [s/{count}records]   {1000 * dt_upd / count:.3f} [ms/records]")

        print("[ ORM UPDATE deferent value ]")
        _, dt_upd = sqlalchemy_orm_update_deferent_values(engine, count)
        print(f"{'%6.2f' % dt_upd} [s/{count}records]   {1000 * dt_upd / count:.3f} [ms/records]")

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
