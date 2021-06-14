"""Sample of try-except."""
import traceback
# import os
# import stat


def main():
    """Run main."""
    try:
        with open("not_found.txt", "r") as _handle:
            pass
    except FileNotFoundError as exc:
        print(f"args={exc.args}")
        print(type(exc))
        print('')
        for attr in dir(exc):
            try:
                if hasattr(exc, str(attr)):
                    print(f"attr={attr}, type={type(getattr(exc, attr))}")
                else:
                    print(f"attr={attr}")

            except AttributeError as exc2:
                print(type(exc2))
                print(traceback.format_exc())
                print(f"attr={attr}")


if __name__ == "__main__":
    main()
