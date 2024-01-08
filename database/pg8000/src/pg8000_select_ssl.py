# -*- coding: utf-8 -*-
"""Example of pg8000 with SSL."""
import os
import ssl
import traceback

import pg8000


def main():
    """Run main."""
    pg_host = os.environ.get("PGHOST")
    pg_database = os.environ.get("PGDATABASE")
    pg_user = os.environ.get("PGUSER")
    pg_password = os.environ.get("PGPASSWORD")

    conn = None
    cur = None
    try:
        pem_path = os.environ.get("PG_SERVER_CERT_PATH")
        ssl_context = ssl.SSLContext()
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        ssl_context.load_verify_locations(pem_path)

        conn = pg8000.connect(
            host=pg_host,
            database=pg_database,
            user=pg_user,
            password=pg_password,
            ssl_context=ssl_context,
        )

        cur = conn.cursor()
        cur.execute("""SELECT * FROM fruits_menu""")
        rows = cur.fetchall()

        for row in rows:
            print(row)

    except pg8000.dbapi.ProgrammingError as exc:
        print(traceback.format_exc())
        print(exc)

    except pg8000.dbapi.DatabaseError as exc:
        print(traceback.format_exc())
        print(exc)

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    main()

# EOF
