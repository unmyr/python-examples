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
                text("SELECT * FROM guest.fruits_menu")
            )
            for row in result:
                print(f"name={row['name']} price={row['price']}", )

    except sqlalchemy.exc.ProgrammingError as exc:
        print(traceback.format_exc())
        print(exc)


if __name__ == '__main__':
    # Note: For backwards compatibility with earlier versions of PostgreSQL,
    # if a root CA file exists, the behavior of sslmode=require will be the
    # same as that of verify-ca, meaning the server certificate is validated
    # against the CA. Relying on this behavior is discouraged,and applications
    # that need certificate validation should always use verify-ca or verify-full.
    engine_psycopg2 = sqlalchemy.create_engine(
        sqlalchemy.engine.URL.create(
            'postgresql+psycopg2',
            host=os.environ.get('PGHOST'),
            port=os.environ.get('PGPORT'),
            database=os.environ.get('PGDATABASE'),
            username=os.environ.get('PGUSER'),
            password=os.environ.get('PGPASSWORD')
        ),
        connect_args={
            'sslmode': 'verify-ca',  # 'require', 'verify-ca', 'verify-full'
            'sslrootcert': os.environ.get('PG_SERVER_CERT_PATH')
        }
    )
    main(engine_psycopg2)

# EOF
