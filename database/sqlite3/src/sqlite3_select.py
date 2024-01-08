"""Example of execute with sqlite3."""
import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE lang (lang_name, lang_age)")

# This is the qmark style:
cur.execute("INSERT INTO lang VALUES (?, ?)", ("C", 49))

# The qmark style used with executemany():
lang_list = [
    ("Fortran", 64),
    ("Python", 30),
    ("Go", 11),
]
cur.executemany("INSERT INTO lang VALUES (?, ?)", lang_list)

# And this is the named style:
cur.execute("SELECT * FROM lang WHERE lang_name=:name AND lang_age=:age", {"name": "C", "age": 49})
print(cur.fetchall())

con.close()
