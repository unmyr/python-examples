"""Example of exception."""
# bar = None
try:
    foo_val = "hello"
    raise RuntimeError('Hello world.')
    bar_val = 'world'  # pylint: disable=unreachable
except RuntimeError as exc:
    print(exc)
finally:
    try:
        print(f"foo_val='{foo_val}' bar_val={bar_val}")
    except NameError:
        print(f"foo_val='{foo_val}' bar_val=undefined")
