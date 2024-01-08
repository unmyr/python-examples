# -*- coding: utf-8 -*-
"""Example of PyGreSQL."""
import os
import traceback

import pg
import pgdb


def main():
    """Run main."""
    pg_host = os.environ.get("PGHOST")
    pg_database = os.environ.get("PGDATABASE")
    pg_user = os.environ.get("PGUSER")
    pg_password = os.environ.get("PGPASSWORD")

    conn = None
    cur = None
    try:
        conn = pgdb.connect(host=pg_host, database=pg_database, user=pg_user, password=pg_password)

        cur = conn.cursor()

        # parameterized queries.
        cur.execute("SELECT * FROM fruits_menu WHERE name = %s", ("Apple",))
        rows = cur.fetchall()
        for row in rows:
            print(row)

    # pylint: disable=no-member
    except pg.InternalError as exc:
        print(type(exc))
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
