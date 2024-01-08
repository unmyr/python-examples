# -*- coding: utf-8 -*-
"""Example of pg8000."""
import os
import traceback

import pg8000.native


def main():
    """Run main."""
    pg_host = os.environ.get("PGHOST")
    pg_database = os.environ.get("PGDATABASE")
    pg_user = os.environ.get("PGUSER")
    pg_password = os.environ.get("PGPASSWORD")

    conn = None
    try:
        conn = pg8000.native.Connection(
            pg_user, host=pg_host, database=pg_database, password=pg_password
        )

        for row in conn.run("""SELECT * FROM fruits_menu"""):
            row_map = {}
            for i, cell in enumerate(row):
                row_map[conn.columns[i].get("name")] = cell
            print(row_map)

    except pg8000.dbapi.ProgrammingError as exc:
        print(traceback.format_exc())
        print(exc)

    except pg8000.dbapi.DatabaseError as exc:
        print(traceback.format_exc())
        print(exc)

    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    main()

# EOF
