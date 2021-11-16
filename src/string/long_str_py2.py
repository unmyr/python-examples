"""Example of long string"""
key_name = 'Apple'
long_str = (
    "SELECT *"
    " FROM fruits_menu"
    " WHERE name='{}'"
).format(key_name)

print(long_str)
assert long_str == "SELECT * FROM fruits_menu WHERE name='Apple'"
