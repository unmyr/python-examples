# -*- coding: utf-8 -*-
"""Example of postgresql+psycopg2."""
import os
import traceback

import sqlalchemy
from sqlalchemy import text


def main(engine):
    """Run main."""
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT * from fruits_menu")
            )
            for row in result:
                print(f"name={row['name']} price={row['price']}", )

    except sqlalchemy.exc.ProgrammingError as exc:
        print(traceback.format_exc())
        print(exc)


if __name__ == '__main__':
    engine_psycopg2 = sqlalchemy.create_engine(
        sqlalchemy.engine.URL.create(
            'postgresql+psycopg2',
            host=os.environ.get('PGHOST'),
            port=os.environ.get('PGPORT'),
            database=os.environ.get('PGDATABASE'),
            username=os.environ.get('PGUSER'),
            password=os.environ.get('PGPASSWORD')
        )
    )
    main(engine_psycopg2)

# EOF
