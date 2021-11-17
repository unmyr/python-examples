"""Example of sqlite3 with SQLAlchemy."""
import os
import time
import traceback
import typing

from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy


Base = declarative_base()


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
    engine.execute(
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
    engine.execute(
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
                session.bulk_save_objects(customers)
                session.commit()
                customers[:] = []
            session.commit()
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

    return dt_ins, t_1 - t_0


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

    try:
        engine = sqlalchemy.create_engine(
            db_uri,
            echo=False
        )

        engine.execute(
            sqlalchemy.text(f"ATTACH DATABASE '{db_name}' AS :schema"),
            schema='guest'
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
        if os.path.exists(db_name):
            os.remove(db_name)


if __name__ == '__main__':
    main()

# EOF
