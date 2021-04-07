# -*- coding: utf-8 -*-
"""Example of psycopg2."""
import os
import traceback

import psycopg2


def main():
    """Run main."""
    pg_host = os.environ.get('PGHOST')
    pg_database = os.environ.get('PGDATABASE')
    pg_user = os.environ.get('PGUSER')
    pg_password = os.environ.get('PGPASSWORD')

    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
            f"host='{pg_host}' dbname='{pg_database}' user='{pg_user}' password='{pg_password}'"
        )
        cur = conn.cursor()
        cur.execute("""SELECT * from fruits_menu""")
        rows = cur.fetchall()
        print("\nShow records:\n")
        for row in rows:
            print("   ", row[0])
    except psycopg2.DatabaseError as exc:
        print(traceback.format_exc())
        print(exc)
    finally:
        if cur is None:
            cur.close()
        if conn is None:
            conn.close()


if __name__ == '__main__':
    main()

# EOF
