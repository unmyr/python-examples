"""Example of sqlite3 with SQLAlchemy."""
import traceback

import sqlalchemy
from sqlalchemy import text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class FruitsMenu(object):
    """OR Mapper for FRUITS_MENU table."""

    # __abstract__ = True


def main(engine):
    """Run main."""
    try:
        with engine.begin() as connection:
            connection.execute(
                sqlalchemy.text("ATTACH DATABASE ':memory:' AS :schema"), {"schema": "guest"}
            )
        metadata = sqlalchemy.MetaData(bind=engine)
        columns = (
            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column("name", sqlalchemy.String(length=16), unique=True),
            sqlalchemy.Column("price", sqlalchemy.Integer),
            sqlalchemy.Column("mod_time", sqlalchemy.DateTime),
        )
        fruit_item_table = sqlalchemy.Table("fruits_menu", metadata, *columns, schema="guest")
        fruit_item_table.create()

        fruit_item_list = [
            {"name": "Apple", "price": 100},
            {"name": "Banana", "price": 120},
            {"name": "Orange", "price": -1},
            {"name": "リンゴ", "price": 180},
        ]
        with engine.begin() as connection:
            connection.execute(
                text("INSERT INTO guest.fruits_menu (name, price) VALUES (:name, :price)"),
                fruit_item_list,
            )
            result = connection.execute(
                text(
                    "SELECT * FROM guest.fruits_menu "
                    "WHERE guest.fruits_menu.name = :name1 OR guest.fruits_menu.name = :name2"
                ),
                {"name1": "Apple", "name2": "Orange"},
            )
            for row in result.mappings():
                print(f"name={row['name']} price={row['price']}")

    except sqlalchemy.exc.ProgrammingError as exc:
        print(traceback.format_exc())
        print(exc)


if __name__ == "__main__":
    engine_sqlite3 = sqlalchemy.create_engine(
        sqlalchemy.engine.URL.create(
            drivername="sqlite", host="", port=None, database=":memory:", username="", password=""
        ),
        echo=False,
    )
    main(engine_sqlite3)

# EOF
