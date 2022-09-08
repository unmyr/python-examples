"""Example of sqlite3 with SQLAlchemy."""
import traceback

import sqlalchemy
from sqlalchemy import text


def main(engine):
    """Run main."""
    try:
        with engine.connect() as connection:
            connection.execute(
                "CREATE TABLE fruits_menu ("
                "  id SERIAL PRIMARY KEY,"
                "  name VARCHAR(16) UNIQUE,"
                "  price INTEGER,"
                "  mod_time timestamp DEFAULT current_timestamp"
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
                    "INSERT INTO fruits_menu (name, price) VALUES (:name, :price)"
                ),
                fruit_item_list
            )
            result = connection.execute(
                text(
                    "SELECT * FROM fruits_menu "
                    "WHERE fruits_menu.name = :name1 OR fruits_menu.name = :name2"
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
            drivername='sqlite',
            host='',
            port=None,
            database=':memory:',
            username='',
            password=''
        ),
        echo=False
    )
    main(engine_sqlite3)

# EOF
