# -*- coding: utf-8 -*-
"""Example of sqlite3 with SQLAlchemy."""
import os
import traceback

import sqlalchemy
from sqlalchemy import text


def main(engine):
    """Run main."""
    try:
        with engine.connect() as connection:
            # cur = connection.cursor()
            connection.execute("CREATE TABLE fruits_menu ("
                               "id SERIAL PRIMARY KEY,"
                               "name VARCHAR(16) UNIQUE,"
                               "price INTEGER,"
                               "modtime timestamp DEFAULT current_timestamp)")

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
                    "INSERT INTO fruits_menu (name, price) VALUES (:name, :price)"
                ),
                fruit_item_list
            )
            result = connection.execute(text("SELECT * FROM fruits_menu"))
            for row in result:
                print(f"name={row['name']} price={row['price']}", )

    except sqlalchemy.exc.ProgrammingError as exc:
        print(traceback.format_exc())
        print(exc)


if __name__ == '__main__':
    engine_sqlite3 = sqlalchemy.create_engine(sqlalchemy.engine.URL.create(
        'sqlite',
        host=os.environ.get(''),
        port=os.environ.get(''),
        database=os.environ.get(':memory:'),
        username=os.environ.get(''),
        password=os.environ.get('')),
        echo=True
    )
    main(engine_sqlite3)

# EOF
