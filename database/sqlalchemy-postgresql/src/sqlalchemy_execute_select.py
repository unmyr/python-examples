# -*- coding: utf-8 -*-
"""Example of postgresql+psycopg2."""
import os
import sys
import traceback
import typing

import sqlalchemy


def setup_sqlite_table(engine: sqlalchemy.engine.base.Engine):
    """Setup sqlite table."""
    try:
        with engine.connect() as connection:
            connection.execute(
                sqlalchemy.text(
                    "ATTACH DATABASE ':memory:' AS :schema"
                ),
                schema='guest'
            )

            # SQLite3 serial type wasn't incremented
            # all of the id element was None
            connection.execute(
                sqlalchemy.text(
                    "CREATE TABLE guest.fruits_menu ("
                    "  id INTEGER PRIMARY KEY,"
                    "  name VARCHAR(16) UNIQUE,"
                    "  price INTEGER,"
                    "  modtime timestamp DEFAULT current_timestamp"
                    ")"
                )
            )

            fruit_item_list: typing.List[dict] = [
                {
                    'name': 'Apple',
                    'price': 100
                },
                {
                    'name': 'Banana',
                    'price': 120
                },
                {
                    'name': 'Orange',
                    'price': 110
                },
                {
                    'name': 'リンゴ',
                    'price': 180
                }
            ]
            connection.execute(
                sqlalchemy.text(
                    "INSERT INTO fruits_menu (name, price) VALUES (:name, :price)"
                ),
                fruit_item_list
            )
    except sqlalchemy.exc.ProgrammingError as exc:
        print(traceback.format_exc())
        print(exc)


def select_all(engine: sqlalchemy.engine.base.Engine) -> typing.List[typing.Tuple]:
    """Run main."""
    try:
        with engine.connect() as connection:
            result = connection.execute(
                sqlalchemy.text("SELECT * FROM guest.fruits_menu")
            )
            values: list = []
            for row in result:
                ary = [None] * len(row)
                for i, cell in enumerate(row):
                    ary[i] = cell
                values.append(tuple(ary))
                print(row)
            return values

    except sqlalchemy.exc.ProgrammingError as exc:
        print(traceback.format_exc())
        print(exc)


def main(driver_name: str) -> typing.NoReturn:
    """Run main."""
    database_url: typing.Optional[str] = None
    if driver_name.startswith('postgresql+'):
        database_url = sqlalchemy.engine.URL.create(
            driver_name,
            host=os.environ.get('PGHOST'),
            port=os.environ.get('PGPORT'),
            database=os.environ.get('PGDATABASE'),
            username=os.environ.get('PGUSER'),
            password=os.environ.get('PGPASSWORD')
        )
    elif driver_name == 'sqlite':
        database_url = sqlalchemy.engine.URL.create(
            driver_name,
            host='',
            port=None,
            database=os.environ.get(':memory:'),
            username='',
            password=''
        )

    connect_args: dict = {}
    if driver_name.startswith('postgresql+psycopg2'):
        # Note: For backwards compatibility with earlier versions of PostgreSQL,
        # if a root CA file exists, the behavior of sslmode=require will be the
        # same as that of verify-ca, meaning the server certificate is validated
        # against the CA. Relying on this behavior is discouraged,and applications
        # that need certificate validation should always use verify-ca or verify-full.
        connect_args = {
            'sslmode': 'verify-ca',  # 'require', 'verify-ca', 'verify-full'
            'sslrootcert': os.environ.get('PG_SERVER_CERT_PATH')
        }
    elif driver_name == 'sqlite':
        connect_args = {}

    engine: sqlalchemy.engine.base.Engine = sqlalchemy.create_engine(
        database_url,
        connect_args=connect_args
    )
    try:
        if driver_name == 'sqlite':
            setup_sqlite_table(engine)
        select_all(engine)
    finally:
        engine.dispose()


if __name__ == '__main__':
    if sys.argv[1] in ['postgresql+pg8000', 'postgresql+psycopg2', 'postgresql+pygresql', 'sqlite']:
        main(sys.argv[1])
    else:
        print(
            f"usage: {sys.argv[0]} "
            '{postgresql+pg8000|postgresql+psycopg2|postgresql+pygresql|sqlite}',
            file=sys.stderr
        )

# EOF
