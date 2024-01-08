# -*- coding: utf-8 -*-
"""Example of pg8000."""
import os
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
        conn = pg8000.connect(
            host=pg_host, database=pg_database, user=pg_user, password=pg_password
        )

        cur = conn.cursor()

        # parameterized queries.
        cur.execute("SELECT * FROM fruits_menu WHERE name = %s", ("Apple",))
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
