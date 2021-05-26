# -*- coding: utf-8 -*-
"""Example of sqlite3 with SQLAlchemy."""
import os
import traceback

from sqlalchemy import text
import sqlalchemy


def main(engine):
    """Run main."""
    try:
        with engine.connect() as connection:
            connection.execute(
                "ATTACH DATABASE ':memory:' AS :schema",
                schema='guest'
            )
            connection.execute(
                "CREATE TABLE guest.fruits_menu ("
                "  id SERIAL PRIMARY KEY,"
                "  name VARCHAR(16) UNIQUE,"
                "  price INTEGER,"
                "  modtime timestamp DEFAULT current_timestamp"
                ")"
            )

            inspector = sqlalchemy.inspect(engine)
            print(f"table_name={inspector.get_table_names()}")

            fruit_item_list = [
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
                    'price': -1
                },
                {
                    'name': 'リンゴ',
                    'price': 180
                }
            ]
            connection.execute(
                text(
                    "INSERT INTO guest.fruits_menu (name, price) VALUES (:name, :price)"
                ),
                fruit_item_list
            )
            result = connection.execute(
                text(
                    "SELECT * FROM guest.fruits_menu "
                    "WHERE guest.fruits_menu.name = :name1 OR guest.fruits_menu.name = :name2"
                ),
                name1='Apple',
                name2='Orange'
            )
            for row in result:
                print(f"name={row['name']} price={row['price']}", )

    except sqlalchemy.exc.ProgrammingError as exc:
        print(traceback.format_exc())
        print(exc)


if __name__ == '__main__':
    engine_sqlite3 = sqlalchemy.create_engine(
        sqlalchemy.engine.URL.create(
            'sqlite',
            host='',
            port=None,
            database=os.environ.get(':memory:'),
            username='',
            password=''
        ),
        echo=False
    )
    main(engine_sqlite3)

# EOF